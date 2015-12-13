from socket import create_connection
from contest.models import Slave
from json import loads, dumps
from question.models import Attempt, AttemptForm 
from threading import Thread
from queue import Queue


def update_marks(profile, attempt):
    return  # NOTE: this is deprecated as we no longer
    # allow attempts on questions which have been answered correctly
    # once
    correct_attempts = Attempt.objects.filter(
        player=profile, question=attempt.question).filter(
            correct=True,).exclude(pk=attempt.pk).count()
    if correct_attempts < 1:  # this has never been correctly attempted
        if attempt.correct:
            profile.score += attempt.marks
            profile.save()


def get_attempt_form(question, player):
    "Get the attempt form prepopulated with last attempt"
    # last attempt
    attempts_on_this_question = Attempt.objects.filter(question=question)
    last_attempts_list = attempts_on_this_question.filter(player=player)
    last_attempt = last_attempts_list.order_by('-stamp').first()
    # generate form
    form = AttemptForm(instance=last_attempt)
    return form
