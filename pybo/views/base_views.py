from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ..models import Question


def index(request):
    page = request.GET.get('page','1') #GET방식으로 호출된 URL에서, page값을 가져올 때 사용, 디폴트값은 1
    kw = request.GET.get('kw', '') #검색어
    question_list = Question.objects.order_by('-create_date') #빠른 시간순으로 정렬
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | #제목 검색
            Q(content__icontains=kw) | #내용 검색
            Q(answer__content__icontains=kw) | #답변 내용 검색
            Q(author__username__icontains=kw) | #질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) #답변 글쓴이 검색
        ).distinct() #중복제거
    paginator = Paginator(question_list, 10) #question_list에서, 페이지당 10개씩 보여준다는 뜻
    page_obj = paginator.get_page(page) # (page)에 해당하는 페이징 객체 생성, 즉 data전체가 아니라 해당 page의 데이터만 조회할 수 있음
    context = {'question_list': page_obj, 'page': page, 'kw': kw} # question_list가 page_obj(페이징 객체)라는 뜻
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)