from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Group, User
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime


def create_paginator(posts_list, request):
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    """Главная страница"""

    posts_list = (Post.objects.all().select_related('author').
                  select_related('group').order_by('-pub_date'))
    page_obj = create_paginator(posts_list, request)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница постов сообщества"""

    group = get_object_or_404(Group, slug=slug)
    posts_list = (Post.objects.filter(group=group).select_related('author').
                  order_by('-pub_date'))
    page_obj = create_paginator(posts_list, request)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Страница пользователя"""

    user = get_object_or_404(User, username=username)
    posts_list = (Post.objects.filter(author=user).select_related('group').
                  order_by('-pub_date'))
    page_obj = create_paginator(posts_list, request)
    context = {
        'page_obj': page_obj,
        'user_fullname': user.get_full_name(),
        'post_cnt': len(posts_list)
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Страница отдельного поста"""

    post = get_object_or_404(Post, pk=post_id).objects.select_related
    user = post.author
    count_posts_user = Post.objects.filter(author=user).count()
    context = {
        'post': post,
        'count_posts_user': count_posts_user,
        'user': user
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Страница создания поста"""

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
                'is_edit': False,
            }
        )
    form = PostForm()
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'is_edit': False,}
    )


@login_required
def post_edit(request, post_id):
    """Страница редактирования поста"""

    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post)
    if post.author.username != request.user.username:
        return redirect('posts:post_detail', post.pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:profile', request.user.username)
        return render(
            request,
            'posts/create_post.html',
            {'form': form,'is_edit': True}
        )
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'is_edit': True
        }
    )