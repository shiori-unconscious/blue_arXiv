from django.shortcuts import render, get_object_or_404
from .models import UserActivity, Paper
import time
from django.db import models


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
    # articles = Paper.objects.all().order_by('-upload_time')[:25]
    articles = Paper.objects.all().order_by('?')[:25]
    for article in articles:
        article.arxiv_id = article.arxiv_id.split('/')[-1]
    return render(request, 'mainpage/index.html', {'articles': articles, 'keywords': [False] * 3})

def user_home(request, username):
    user_activity = UserActivity.objects.filter(user__username=username).first()
    if user_activity is not None:
        liked_content = user_activity.liked_content.all()
        bookmarked_content = user_activity.bookmarked_content.all()
        return render(request, 'mainpage/user_home.html', {'liked_content': liked_content, 'bookmarked_content': bookmarked_content})
    return render(request, 'mainpage/user_home.html', {'liked_content': [], 'bookmarked_content': []})

def search(request):
    keywords = [False] * 3
    if request.method == 'POST':
        search_keyword = request.POST.get('search_keyword')
        search_field = request.POST.get('search_field')

        if search_field == 'title':
            papers = Paper.objects.filter(title__icontains=search_keyword)[:25]
            keywords[0] = True
        elif search_field == 'author':
            papers = Paper.objects.filter(authors__icontains=search_keyword)[:25]
            keywords[1] = True
        elif search_field == 'abstract':
            papers = Paper.objects.filter(abstract__icontains=search_keyword)[:25]
            keywords[2] = True
        else:
            papers = Paper.objects.filter(
                models.Q(title__icontains=search_keyword) |
                models.Q(authors__icontains=search_keyword) |
                models.Q(abstract__icontains=search_keyword)
            )[:25]
            keywords = [True] * 3
    else:
        papers = Paper.objects.all().order_by('-upload_time')[:25]
    for paper in papers:
        paper.arxiv_id = paper.arxiv_id.split('/')[-1]
        
    return render(request, 'mainpage/index.html', {'articles': papers, 'keywords': keywords, 'keyword': search_keyword})