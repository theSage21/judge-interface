from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from question import models
from django.http import JsonResponse
from question import functions
from contest.functions import is_contest_on


def leaderboard(request):
    """The scoreboard"""
    data = {}
    template = 'question/leaderboard.html'
    data['players'] = models.Profile.objects.order_by('-score')
    data['questions'] = models.Question.objects.order_by('qno')
    data['contest_on'] = is_contest_on()
    return render(request, template, data)


def question_home(request):
    """Show all questions"""
    data = {}
    template = 'question/question.html'
    data['questions'] = models.Question.objects.all()
    data['contest_on'] = is_contest_on()
    return render(request, template, data)


@login_required
def question(request, qno):
    """Display a question and the form to accept the user's answer"""
    qno = int(qno)
    data = {}
    template = 'question/question.html'
    data['contest_on'] = is_contest_on()
    ques = get_object_or_404(models.Question, qno=qno)
    if is_contest_on() or ques.practice:
        data['question'] = ques
        data['marks'] = functions.get_marks(data['question'])
        data['attempts'] = models.Attempt.\
            objects.filter(question=data['question'],
                           player=request.user.profile).order_by('-stamp')
        for att in data['attempts']:
            if att.correct is None:
                functions.is_correct(att)
        if len(data['attempts']) > 0:
            last_correct = data['attempts'][0].correct
        else:
            last_correct = False
        data['last_correct'] = last_correct

        if request.method == 'GET':
            data['answer_form'] = functions.get_attempt_form(
                ques, request.user.profile)
        if request.method == 'POST':
            data['answer_form'] = models.AttemptForm(
                request.POST, request.FILES)
            if data['answer_form'].is_valid():
                form = data['answer_form']
                attempt = form.save(commit=False)
                attempt.player = request.user.profile
                attempt.question = data['question']
                attempt.marks = data['marks']
                attempt.save()
                if functions.is_correct(attempt):  # force a check request
                    functions.update_marks(request.user.profile, attempt)
                return redirect('question:question', qno=qno)

    return render(request, template, data)


def question_details(request, qno):
    """
    Details pertaining to a question to be used by the
    Check server
    """
    data = {}
    qno = int(qno)
    question = get_object_or_404(models.Question, qno=qno)
    #  -----
    data['inp'] = question.answer.infile.url
    data['out'] = question.answer.outfile.url
    data['type'] = question.answer.answer_type.pk
    return JsonResponse(data)


def attempt(request, att):
    data, att = {}, int(att)
    template = 'question/attempt.html'
    # -----
    attempt = get_object_or_404(models.Attempt, pk=att)
    data['attempt'] = attempt
    data['contest_on'] = is_contest_on()
    return render(request, template, data)


def language_details(request, lno):
    """
    Language details to be use by the Check server
    """
    data = {}
    lno = int(lno)
    language = get_object_or_404(models.Language, lno=lno)
    # -----
    data['wrap'] = language.wrapper.url
    data['misc'] = language.details
    return JsonResponse(data)


def detail_list(request):
    """
    A JSON containing all details pertaining to all questions
    and languages on the server
    """
    data = {}
    questions = models.Question.objects.all()
    data['question'] = {}
    for q in questions:
        data['question'][str(q.pk)] = {'inp': q.answer.infile.url,
                                       'out': q.answer.outfile.url,
                                       'type': q.answer.answer_type.pk
                                       }
    languages = models.Language.objects.all()
    data['language'] = {}
    for l in languages:
        data['language'][str(l.pk)] = {'wrap': l.wrapper.url,
                                       'misc': l.details,
                                       'overwrite': l.overwrite
                                       }
    return JsonResponse(data)
