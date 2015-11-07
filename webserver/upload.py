import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
import django
django.setup()

from django.core.files import File
from question.models import Answer, Question, AnswerType

def read(qno, filename):
    path = os.path.join(str(qno), filename)
    with open(path, 'r') as fl:
        data = fl.read()
    return data

print('Adding questions')
questions = '1234567'
for ques in questions:
    q = Question()
    q.qno = int(ques)
    q.title = read(ques, 'title')
    q.text = read(ques, 'text')
    if (q == '1') or (q == '2'):
        q.practice = True
    q.save()
    ans = Answer()
    ans.question = q
    ans.infile = File(open(ques + '/inp', 'r'))
    ans.outfile = File(open(ques + '/out', 'r'))
    ans.sample_code = File(open(ques + '/sample', 'r'))
    ans.answer_type = AnswerType.objects.first()
    ans.save()
