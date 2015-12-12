from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.forms import ModelForm


class Profile(User):
    """
    A user profile.
    Stores scores and other data
    """
    last_solved = models.DateTimeField(default=now)

    def _get_score(self):
        "Get the user's current score"
        attempts = Attempt.objects.filter(player=self).filter(correct=True)
        score = attempts.aggregate(models.Sum('marks'))
        print(score, 'score')
        marks = score['marks__sum']
        return marks if marks is not None else 0
    score = property(_get_score)


class Language(models.Model):
    """A programming language which is available on the check server.
    """
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    details = models.TextField()
    wrapper = models.FileField(upload_to='wrappers')
    overwrite = models.BooleanField(default=False,
                                    help_text='overwrite required\
                                    for storing the source code')


class Attempt(models.Model):
    """An attempt on a question"""
    def __str__(self):
        return self.question.__str__() + ' - ' + self.player.__str__()
    player = models.ForeignKey('Profile', related_name='player')
    question = models.ForeignKey('Question', related_name='question')
    language = models.ForeignKey('Language', related_name='language')
    source = models.TextField(null=True)
    source_name = models.CharField(max_length=30,
                                   help_text='Name of source code file',
                                   null=True)
    correct = models.NullBooleanField(default=None)
    stamp = models.DateTimeField(auto_now_add=True)
    marks = models.FloatField()
    remarks = models.TextField()  # Remarks from the check server go there

    def get_absolute_url(self):
        "Get the absolute url of the attempt"
        return reverse('question:attempt', kwargs={'att': self.pk})

    def get_json__(self):
        """
        Return essential data as dict
        """
        data = {'pk': self.pk,
                'qno': self.question.pk,
                'source': self.source,
                'name': self.source_name,
                'language': self.language.pk,
                }
        return data

    def is_correct(self):
        """Checks if the attempt was correct
        By contacting the check server."""
        if self.correct is not None:
            return self.correct
        else:
            data = self.get_json__()
            t = Thread(target=ask_check_server, args=(data,))
            t.start()
            global result_Q
            results = {}
            while result_Q.qsize() > 0:
                key, val, rem = result_Q.get()
                results[key] = (val, rem)
            pk = data['pk']
            result, comment = None, "Checking..."
            for key, value in results.items():
                if key == pk:
                    result, comment = value
                else:
                    result_Q.put((key, value[0], value[1]))
            self.correct = result
            self.remarks = comment
            self.marks = self.question.get_marks()
            self.save()
            return attempt.correct


class Question(models.Model):
    """A question in the competition"""
    qno = models.IntegerField()
    title = models.CharField(max_length=50)
    text = models.TextField(default='Question text goes here')
    practice = models.BooleanField(default=False)
    # -----------

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question:question', kwargs={'qno': self.qno})

    def has_been_answered(self, user):
        attempts = Attempt.objects.filter(question=self, player=user.profile)
        for att in attempts:
            functions.is_correct(att)
        return any([i.correct for i in attempts])


    def get_marks(self):
        """Get the current score for a question"""
        if self.practice:
            return 0
        total_attempts = Attempt.objects.filter(
            question=self).exclude(correct=None).count()
        if total_attempts == 0:
            score = 1.0
        else:
            wrong_attempts = Attempt.objects.filter(
                question=self, correct=False).count()
            score = float(wrong_attempts) / float(total_attempts)
        return score

class AnswerType(models.Model):
    """Used to determine which type of checking to use.
    Error tolerant or exact.
    For future use."""

    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)


class Answer(models.Model):
    """The answer to a question"""
    def __str__(self):
        return self.question.__str__()
    question = models.OneToOneField(Question)
    infile = models.FileField(upload_to='test_cases')
    outfile = models.FileField(upload_to='test_cases')
    sample_code = models.FileField(upload_to='solutions')
    answer_type = models.ForeignKey(AnswerType, related_name='answer_type')


class AttemptForm(ModelForm):
    class Meta:
        model = Attempt
        exclude = ['player', 'question', 'stamp',
                   'correct', 'marks', 'remarks']
