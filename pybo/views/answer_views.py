from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


#답변 등록 방법 1 : question에서 answer을 사용(Question과 Answer이 서로 Foreignkey로 연결되어 있어서 가능)
#                   >> question.answer_set을 사용
@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록 부분
    """
    #ex) http://localhost:8000/pybo/answer/create/2/라는 페이지를 요청하면 question_id에는 2가 전달됨
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정(request.user) 저장
            answer.create_date =timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # #question.answer_set >> 질문의 답변을 의미함
    # return redirect('pybo:detail', question_id=question.id)
'''
#답변 등록 방법 2 : Question과 Answer을 따로따로 사용
#                 >> from .models import Question,Answer

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer(question = question, content=request.POST.get('content'),
             create_date=timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id=question.id)
'''

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


#답변 추천 함수
@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작승한 글은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

















