from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin, name='admin'),
    path('admin/posts/', views.admin_posts, name='admin_posts'),
    path('admin/post/<int:post_id>/', views.admin_post_detail, name='admin_post_detail'),
    path('admin/post/create/', views.create_post, name='create_post'),
    path('admin/post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('admin/post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('admin/comment/show/<int:comment_id>/', views.hide_comment, name='hide_comment'),
    path('admin/comment/hide/<int:comment_id>/', views.show_comment, name='show_comment'),
    path('admin/user/', views.admin_user, name='admin_user'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('login/', views.bu_login, name='login'),
    path('logout/', views.bu_logout, name='logout'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('unlike/<int:post_id>/', views.unlike, name='unlike'),
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('search/', views.search, name='search'),
]
