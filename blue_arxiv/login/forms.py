from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "账号密码的对应不正确😭",
        "inactive": "这个账号不能登录",
    }

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages['unique'] = '该用户名已经被使用，请选择一个不同的用户名'
        
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields
        