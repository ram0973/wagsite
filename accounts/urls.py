"""
This is auth module urls
"""
from django.urls import path
from . import views as auth_views

urlpatterns = [
    path('<slug:username>/', auth_views.user_view, name='user_view'),
]
