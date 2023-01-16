from django.db import models
from django.contrib.auth.models import User  #회원 가입시 데이터 저장에 사용했던 모델
# Create your models here.

#질문 모델
class Question(models.Model):
    #글쓴이 속성(author field) 추가
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
            #on_delete=models.CASCADE >>> 계정이 삭제되면, 그 계정이 작성한 질문을 모두 삭제
            #, null=True를 입력하여, null속성을 허용 할 수도 있다.
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') #추천인 추가

    def __str__(self):
        return self.subject

#답변 모델
class Answer(models.Model):
    #글쓴이 속성(author field) 추가
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True) #null=True는 DB상에서 null을 허용,
                                                              #blank=True는 form.is_valid()를 통한 입력값 검증시, 값이 없어도 됨을 의미
                                                              #>>> 즉, 수정한 경우에만 생성되는 데이터이므로, 빈 값으로 놔둘 수 있게 설정했음
    voter = models.ManyToManyField(User, related_name='voter_answer')



