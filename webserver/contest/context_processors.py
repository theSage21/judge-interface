from contest import models
from django.utils import timezone
from contest.functions import is_contest_on, contest_phase


def contest_time(request):
    context = {}
    now = timezone.now()
    contest = models.ContestControl.objects.first()
    if now < contest.start:
        time = contest.start
    elif contest.start <= now <= contest.end:
        time = contest.end
    else:
        time = None
    context['contest_time'] = time
    context['contest_on'] = is_contest_on()
    context['contest_phase'] = contest_phase()
    return context
