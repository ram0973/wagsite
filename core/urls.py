""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from core.views import home, markdown_uploader

urlpatterns = [
    #path('', home, name='home'),
    path('api/uploader/', markdown_uploader, name='markdown_uploader_page'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # path('auth/', include('django.contrib.auth.urls')),
    # login/, name='login'
    # logout/, name='logout'

    # password_change/, name='password_change'
    # password_change/done/, name='password_change_done'

    # password_reset/, name='password_reset'
    # password_reset/done/, name='password_reset_done'
    # reset/<uidb64>/<token>/, name='password_reset_confirm'
    # reset/done/, name='password_reset_complete

    path('blog/', include('blog.urls', namespace='blog')),
    path('martor/', include('martor.urls')),

    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),


]

# if os.getenv('DJANGO_CONFIGURATION') == 'Dev':
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.ASSETS_URL,
#                           document_root=settings.ASSETS_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
#     urlpatterns += static('/favicon.ico',
#                           document_root='{}{}'.format(settings.PUBLIC_DIR,
#                                                       '/favicon.ico'))
