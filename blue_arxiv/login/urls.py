from django.urls import path
from .views import user_login, register, check_username


urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('register/', register, name="register"),
    path('check_username/', check_username, name="check_username"),
]