from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
        # password1은 비밀번호, password2는 대조값이다
        # email같이 새로운 속성을 추가하려면, UserCreationForm을 그대로 사용하는것이 아니라, 상속받아서 새로 생성하여야 한다

