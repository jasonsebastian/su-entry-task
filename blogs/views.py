from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import BlogUserForm, CommentForm
from .models import BlogUser, Comment, Post


def index(request):
    context = {'posts': Post.objects.all()}
    if request.user.is_authenticated:
        context['bu'] = get_object_or_404(BlogUser, user=request.user)
    else:
        context['user_form'] = BlogUserForm()

    return render(request, 'blogs/index.html', context)


def bu_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

    return HttpResponseRedirect('/blogs/')


def bu_logout(request):
    logout(request)
    return HttpResponseRedirect('/blogs/')


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
    context = {
        'comment_form': CommentForm(),
        'post': get_object_or_404(Post, post_id=post_id),
    }

    if request.user.is_authenticated:
        context['bu'] = get_object_or_404(BlogUser, user=request.user)
    else:
        context['user_form'] = BlogUserForm()

    return render(request, 'blogs/comments.html', context)


def add_comment(request, post_id):
    if request.method == 'POST':
        user = get_object_or_404(BlogUser, user=request.user)
        post = get_object_or_404(Post, post_id=post_id)
        comment_content = request.POST['comment_content']
        c = Comment(user=user, post=post, comment_content=comment_content)
        c.save()
        return HttpResponseRedirect('/blogs/')


def search(request):
    query = request.GET.get("q")
    print(type(query))
    context = dict()

    try:
        results = Post.objects.filter(Q(post_title__icontains=query) | Q(post_content__icontains=query)).values()
        context['results'] = results
    except Post.DoesNotExist:
        context['results'] = None

    if request.user.is_authenticated:
        context['bu'] = get_object_or_404(BlogUser, user=request.user)
    else:
        context['user_form'] = BlogUserForm()

    return render(request, 'blogs/search.html', context)


@login_required
def admin(request):
    return HttpResponseRedirect('/blogs/admin/posts')


def admin_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/blogs/admin')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)

        return HttpResponseRedirect('/blogs/admin/')

    return render(request, 'blogs/admin_login.html')


@login_required
def admin_posts(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)
    
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blogs/admin_posts.html', {'posts': posts})


@login_required
def admin_user(request):
    return render(request, 'blogs/admin_user.html')
