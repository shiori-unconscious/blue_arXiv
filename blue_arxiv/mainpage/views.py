from django.shortcuts import render
from .models import Paper
from django.db import models
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .recommend import Recommend

@login_required
def delete(request, papername):
    user_model = request.user
    if Paper.objects.filter(arxiv_id=papername).exists():
        if user_model.liked_content.filter(arxiv_id=papername).exists():
            user_model.liked_content.get(arxiv_id=papername).delete()
        if user_model.disliked_content.filter(arxiv_id=papername).exists():
            user_model.disliked_content.get(arxiv_id=papername).delete()
    
    return user_home(request)

@login_required
def neg(request, papername):
    user_model = request.user
    paper = Paper.objects.get(arxiv_id=papername)
    if paper:
        if user_model.liked_content.filter(arxiv_id=papername).exists():
            user_model.liked_content.get(arxiv_id=papername).delete()            
        if paper not in user_model.disliked_content.all():
            user_model.disliked_content.add(paper)
    articles = Paper.objects.all().order_by('?')[:10]
    for article in articles:
        article.arxiv_id = article.arxiv_id.split('/')[-1]
    return render(request, 'mainpage/index.html', {'articles': articles})

@login_required
def vote(request, papername):
    user_model = request.user
    paper = Paper.objects.get(arxiv_id=papername)
    if paper:
        if user_model.disliked_content.filter(arxiv_id=papername).exists():
            user_model.disliked_content.get(arxiv_id=papername).delete()            
        if paper not in user_model.liked_content.all():
            user_model.liked_content.add(paper)
    articles = Paper.objects.all().order_by('?')[:10]
    for article in articles:
        article.arxiv_id = article.arxiv_id.split('/')[-1]
    return render(request, 'mainpage/index.html', {'articles': articles})


def main_page(request):
    if request.user.is_authenticated:
        recommend = Recommend(request.user)
        articles = recommend.recommend()
    else:
        articles = Paper.objects.all().order_by('?')[:25]
    for article in articles:
        article.arxiv_id = article.arxiv_id.split('/')[-1]
    return render(request, 'mainpage/index.html', {'articles': articles, 'keywords': [False] * 3})

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

@login_required
def user_home(request):
    user_model = request.user
    return render(request, 'mainpage/user_home.html', {'liked_content': user_model.liked_content.all(), 'disliked_content': user_model.disliked_content.all(), 'username': user_model.username})    