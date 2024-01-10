from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from .models import CustomUser
import json

@require_POST
def check_username(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        username_exists = CustomUser.objects.filter(username=username).exists()
        response_data = {'username_exists': username_exists}
        return JsonResponse(response_data)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            # 获取表单中的用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 使用 authenticate() 进行用户认证
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # 使用 login() 登录用户
                login(request, user)
                return redirect('/')  # 登录成功后重定向到成功页面
        
        else:
            return render(request, 'login/login.html', {'form' : form})
        
    form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            print(form.errors.as_text())
    else:   
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})