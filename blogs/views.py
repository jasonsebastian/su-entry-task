from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from .forms import BlogUserLoginForm, CommentForm, CreatePostForm, EditPostForm, BlogUserCreationForm
from .models import BlogUser, Comment, Post


def index(request):
    context = {
        'posts': Post.objects.annotate(
            visible_comments=Count('comment', filter=Q(comment__is_hidden=False))
        )
    }

    if request.user.is_authenticated:
        context['bu'] = get_object_or_404(BlogUser, user=request.user)
    else:
        context['user_form'] = BlogUserLoginForm()

    return render(request, 'blogs/index.html', context)


def bu_login(request):
    if request.method == 'POST':
        form = BlogUserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Welcome back, {}!".format(user.first_name))
                return redirect('blogs:index')

        messages.add_message(request, messages.ERROR, "Incorrect username or password.")

    return redirect('blogs:index')


def bu_logout(request):
    logout(request)
    return redirect('blogs:index')


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


def post_detail(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            user = get_object_or_404(BlogUser, user=request.user)
            post = get_object_or_404(Post, post_id=post_id)
            comment_content = request.POST['comment_content']
            c = Comment(user=user, post=post, comment_content=comment_content)
            c.save()
            messages.add_message(request, messages.SUCCESS, "You have successfully commented on this post!")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Oops, it looks like your comment is invalid. Please try again!")

    post = get_object_or_404(Post, post_id=post_id)
    comments = post.comment_set.all().filter(is_hidden=False)

    context = {
        'comment_form': CommentForm(),
        'post': post,
        'visible_comments': comments
    }

    if request.user.is_authenticated:
        context['bu'] = get_object_or_404(BlogUser, user=request.user)
    else:
        context['user_form'] = BlogUserLoginForm()

    return render(request, 'blogs/post_details.html', context)


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
        context['user_form'] = BlogUserLoginForm()

    return render(request, 'blogs/search.html', context)


@staff_member_required(login_url='blogs:admin_login')
def admin(request):
    return redirect('blogs:admin_posts')


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('blogs:admin')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)

        return redirect('blogs:admin')

    return render(request, 'blogs/admin_login.html')


@staff_member_required(login_url='blogs:admin_login')
def admin_posts(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    return render(request, 'blogs/admin_posts.html', {
        'posts': paginator.get_page(page)
    })


@staff_member_required(login_url='blogs:admin_login')
def admin_post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blogs/admin_post_detail.html', {'post': post})


@staff_member_required(login_url='blogs:admin_login')
def hide_comment(request, comment_id):
    c = get_object_or_404(Comment, pk=comment_id)

    if not c.is_hidden:
        c.is_hidden = True
        c.save()

    if 'blogs/admin/post/' in request.META['HTTP_REFERER']:
        return redirect('blogs:admin_post_detail', post_id=c.post.post_id)
    elif 'blogs/admin/user/' in request.META['HTTP_REFERER']:
        return redirect('blogs:admin_user_detail', username=c.user.user.username)


@staff_member_required(login_url='blogs:admin_login')
def show_comment(request, comment_id):
    c = get_object_or_404(Comment, pk=comment_id)

    if c.is_hidden:
        c.is_hidden = False
        c.save()

    if 'blogs/admin/post/' in request.META['HTTP_REFERER']:
        return redirect('blogs:admin_post_detail', post_id=c.post.post_id)
    elif 'blogs/admin/user/' in request.META['HTTP_REFERER']:
        return redirect('blogs:admin_user_detail', username=c.user.user.username)

    return redirect('blogs:admin_post_detail', c.post.post_id)


@staff_member_required(login_url='blogs:admin_login')
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post_title = request.POST['post_title']
            post_content = request.POST['post_content']
            p = Post(post_title=post_title, post_content=post_content)
            p.save()
            messages.add_message(request, messages.SUCCESS, "You have succesfully created a post!")
            return redirect('blogs:admin_posts')
        else:
            messages.add_message(request, messages.ERROR, "Invalid post title and post content.")

    return render(request, 'blogs/admin_create_post.html', {
        'create_post_form': CreatePostForm()
    })


@staff_member_required(login_url='blogs:admin_login')
def edit_post(request, post_id):
    if request.method == 'POST':
        form = EditPostForm(request.POST)
        if form.is_valid():
            p = get_object_or_404(Post, pk=post_id)
            p.post_title = request.POST['post_title']
            p.post_content = request.POST['post_content']
            p.save()
            messages.add_message(request, messages.SUCCESS, "You have succesfully edited a post!")
            return redirect('blogs:admin_posts')

        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, "Invalid post title and post content.")

    post = get_object_or_404(Post, pk=post_id)

    return render(request, 'blogs/admin_edit_post.html', {
        'edit_post_form': EditPostForm(initial={
            'post_title': post.post_title,
            'post_content': post.post_content,
        })
    })


@staff_member_required(login_url='blogs:admin_login')
def delete_post(request, post_id):
    if request.method == 'POST':
        get_object_or_404(Post, pk=post_id).delete()

    return redirect('blogs:admin_posts')


@staff_member_required(login_url='blogs:admin_login')
def admin_user(request):
    user_list = BlogUser.objects.all()
    paginator = Paginator(user_list, 5)

    page = request.GET.get('page')
    return render(request, 'blogs/admin_user.html', {
        'users': paginator.get_page(page)
    })


@staff_member_required(login_url='blogs:admin_login')
def admin_user_detail(request, username):
    return render(request, 'blogs/admin_user_detail.html', {
        'bu': get_object_or_404(BlogUser, user__username=username)
    })


@staff_member_required(login_url='blogs:admin_login')
def create_user(request):
    if request.method == 'POST':
        form = BlogUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                request.POST['username'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
            )
            user.save()

            bu = BlogUser(user=user, matric_no=request.POST['matric_no'])
            bu.save()
            messages.add_message(request, messages.SUCCESS, "You have successfully registered a user!")
            return redirect('blogs:admin_user')
        else:
            messages.add_message(request, messages.ERROR, "Invalid entries.")

    return render(request, 'blogs/admin_create_user.html', {
        'create_user_form': BlogUserCreationForm()
    })
