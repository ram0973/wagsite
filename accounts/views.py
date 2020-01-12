from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()


def user_view(request, username):
    user = User.objects.filter(is_active=True, email=username).first()
    return render(request, 'accounts/user_view.html', {'user': user})
