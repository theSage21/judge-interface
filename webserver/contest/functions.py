from contest.models import ContestControl
from django.utils import timezone


def is_contest_on():
    contest = ContestControl.objects.first()
    now = timezone.now()
    if contest.start <= now <= contest.end:
        return True
    return False


def contest_phase():
    now = timezone.now()
    contest = ContestControl.objects.first()
    if now < contest.start:
        return 'before'
    elif contest.start <= now <= contest.end:
        return 'during'
    elif contest.end < now:
        return 'after'
