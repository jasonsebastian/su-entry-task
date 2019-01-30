from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.bu_login, name='login'),
    path('logout/', views.bu_logout, name='logout'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('unlike/<int:post_id>/', views.unlike, name='unlike'),
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
