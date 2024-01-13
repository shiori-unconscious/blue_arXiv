from django.urls import path
from .views import main_page, user_home, vote, neg, search, delete
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', main_page, name='main_page'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('user_home/', user_home, name='user_home'),
    path('vote/<str:papername>', vote, name='vote'),
    path('neg/<str:papername>', neg, name='neg'),
    path('search/', search, name="search"),
    path('remove/<str:papername>', delete, name="remove"),
]