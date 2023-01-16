from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST) #request.POST에 담긴 subject와 content가 QuestionForm에 자동으로 저장되어 객체가 생성됨
        if form.is_valid(): #폼이 유효하다면
            question = form.save(commit=False) #commit=False를 통해 임시저장하여 question 객체를 리턴받음
            question.author = request.user # author 속성에 로그인 계정 저장
            question.create_date = timezone.now() #실제 저장을 위해 작성일시를 설정, 데이터 저장 시점에 생성해야 하므로 QuestionForm에 등록하지 않는다
            question.save() #데이터를 실제로 저장

            return redirect('pybo:index')
    else: # request.method == 'GET'인 경우
        form = QuestionForm() # >> 질문을 등록하는 화면을 렌더링함
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다') #넌필드 오류를 발생시킬 경우에 사용
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST": #질문을 수정하고 "저장하기"를 누르면 POST방식으로 호출됨(form태그에 action 속성이 없어서, default action이 현재 페이지가 되기 때문)
        form = QuestionForm(request.POST, instance=question) #수정된 내용을 반영하기위해 이와 같이 폼을 생성한다
        # >>> instance를 기준으로 QuestionForm을 생성하지만, request.POST로 덮어쓰라는 의미
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() #수정 일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:# "수정" 버튼을 누르면 GET방식 호출
        form = QuestionForm(instance=question) # >> 질문수정 화면에 그 질문의 제목과 내용이 반영되어야 하므로 instance=question으로 속성을 채움

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

# 질문추천 함수 >> 동일한 사용자가 해당 질문에 여러번 추천하더라도 추천수가 증가하지 않는다.
@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)