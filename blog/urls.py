from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-index'),
    # path('articles/<int:year>/', views.year_archive),
    # path('articles/<int:year>/<int:month>/', views.month_archive),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.PostDateDetailView.as_view(date_field='pub_date'),
         name='post-details'),
]
