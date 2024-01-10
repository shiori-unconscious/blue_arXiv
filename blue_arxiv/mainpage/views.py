from django.shortcuts import render, get_object_or_404
from .models import UserActivity, Paper
from django.views.generic import TemplateView
import time

def neg(request, papername):
    time.sleep(2)
    articles = Paper.objects.all().order_by('?')[:10]
    for article in articles:
        article.arxiv_id = article.arxiv_id.split('/')[-1]
    return render(request, 'mainpage/index.html', {'articles': articles})

def vote(request, papername):
    time.sleep(3)
    articles = Paper.objects.all().order_by('?')[:10]
    for article in articles:
        article.arxiv_id = article.arxiv_id.split('/')[-1]
    return render(request, 'mainpage/index.html', {'articles': articles})


def main_page(request):
    articles = Paper.objects.all().order_by('upload_time')[:10]
    for article in articles:
        article.arxiv_id = article.arxiv_id.split('/')[-1]
    return render(request, 'mainpage/index.html', {'articles': articles})

def user_home(request, username):
    user_activity = UserActivity.objects.filter(user__username=username).first()
    if user_activity is not None:
        liked_content = user_activity.liked_content.all()
        bookmarked_content = user_activity.bookmarked_content.all()
        return render(request, 'mainpage/user_home.html', {'liked_content': liked_content, 'bookmarked_content': bookmarked_content})
    return render(request, 'mainpage/user_home.html', {'liked_content': [], 'bookmarked_content': []})
    