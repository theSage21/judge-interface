from socket import create_connection
from contest.models import Slave
from json import loads, dumps
from question.models import Attempt, AttemptForm
from threading import Thread
from queue import Queue

result_Q = Queue()


def get_alive_slaves():
    "No of slaves alive"
    slaves = Slave.objects.all()
    alive = [s for s in slaves if s.is_alive()]
    return alive


def assign_job(data, jobs={}):
    """
    Assign the job to some slave in the available list.
    """
    pk = data['pk']
    is_assigned = pk in jobs.keys()
    assignment_needed = False
    if is_assigned:
        slave = jobs[pk]
        if not slave.is_alive():
            assignment_needed = True
    else:
        assignment_needed = True

    if assignment_needed:
        slaves = get_alive_slaves()
        # if slaves: what if there are no slaves?
        assigned = False
        while not assigned:  # assign to first non busy slave
            for slave in slaves:
                if not slave.busy:
                    jobs[pk] = slave
                    assigned = True
    address = jobs[pk].get_address()
    return jobs[pk], address


def ask_check_server(data):
    """
    Ask the check server is the current attempt done?
    Returns None/True/False and comments.
    data is of type
        data = {
            'pk'        :primary key of attempt,
            'qno'       :question number pk,
            'source'    :source code,
            'name'      :name of file,
            'language'  :language pk,
            }
    """
    slave, address = assign_job(data)

    with slave:
        try:
            sock = create_connection(address)
        except:
            value, remarks = None, 'Connection error'
        else:
            data = dumps(data)
            sock.sendall(data.encode('utf-8'))
            resp = sock.recv(4096)
            resp, remarks = loads(resp.decode())
        finally:
            sock.close()

    if resp == 'Timeout':
        value, remarks = False, resp
    elif resp == 'Correct':
        value, remarks = True, resp
    elif resp == 'Incorrect':
        value, remarks = False, resp
    elif resp == 'Error':
        value, remarks = False, remarks
    global result_Q
    data = loads(data)
    result_Q.put((data['pk'], value, remarks))


def is_correct(attempt):
    """Checks if the attempt was correct
    By contacting the check server."""
    if attempt.correct is not None:
        return attempt.correct
    else:
        data = attempt.get_json__()
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

        attempt.correct = result
        attempt.remarks = comment
        attempt.marks = get_marks(attempt.question)
        attempt.save()
        return attempt.correct


def get_marks(question):
    """Get the current score for a question"""
    if question.practice:
        return 0
    total_attempts = Attempt.objects.filter(
        question=question).exclude(correct=None).count()
    wrong_attempts = Attempt.objects.filter(
        question=question, correct=False).count()
    if total_attempts == 0:
        score = 1.0
    else:
        score = float(wrong_attempts) / float(total_attempts)
    return score


def update_marks(profile, attempt):
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
