from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import BlogUserForm, CommentForm
from .models import BlogUser, Comment, Post


def index(request):
    if request.user.is_authenticated:
        return render(request, 'blogs/index.html', {
            'bu': get_object_or_404(BlogUser, user=request.user),
            'posts': Post.objects.all(),
        })

    return render(request, 'blogs/index.html', {
        'user_form': BlogUserForm(),
        'posts': Post.objects.all()
    })


def bu_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', '/'))


def bu_logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def like(request, post_id):
    bu = get_object_or_404(BlogUser, user=request.user)
    p = get_object_or_404(Post, post_id=post_id)
    if p not in bu.liked_posts.all():
        bu.liked_posts.add(p)
        bu.save()
    return HttpResponseRedirect(request.GET.get('next', '/'))


def unlike(request, post_id):
    bu = get_object_or_404(BlogUser, user=request.user)
    p = get_object_or_404(Post, post_id=post_id)
    if p in bu.liked_posts.all():
        bu.liked_posts.remove(p)
        bu.save()
    return HttpResponseRedirect(request.GET.get('next', '/'))


def comment(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    if request.user.is_authenticated:
        return render(request, 'blogs/comments.html', {
            'bu': get_object_or_404(BlogUser, user=request.user),
            'comment_form': CommentForm(),
            'post': post,
        })

    return render(request, 'blogs/comments.html', {
        'user_form': BlogUserForm(),
        'comment_form': CommentForm(),
        'post': post,
    })


def add_comment(request, post_id):
    if request.method == 'POST':
        user = get_object_or_404(BlogUser, user=request.user)
        post = get_object_or_404(Post, post_id=post_id)
        comment_content = request.POST['comment_content']
        c = Comment(user=user, post=post, comment_content=comment_content)
        c.save()
        return HttpResponseRedirect('/blogs/')

