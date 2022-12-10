from .models import Group, Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail

# ctraniza
def index(request):
    template = 'posts/index.html'
    content = 'Это главная страница проекта Yatube'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'content': content,
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    content = 'Здесь будет информация о группах проекта Yatube'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'content': content,
        'page_obj': page_obj
    }

    return render(request, template, context)


def profile(request, username):
    post_list = Post.objects.filter(author__username=username)
    first_post = post_list[0]
    rest_posts = post_list[1:]
    paginator = Paginator(rest_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    col_posts = len(post_list)

    context = {
        'author': first_post.author,
        'first_post': first_post,
        'page_obj': page_obj,
        'col_posts': col_posts
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    title = post.text[:30]
    col_posts = Post.objects.filter(author__username=post.author).count()

    context = {
        'post': post,
        'title': title,
        'col_posts': col_posts
    }

    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    content = 'Новая запись'
    url = '/create/'

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()

            return redirect('posts:profile', request.user.username)

        return render(request, 'contact.html', {'content': content, 'form': form, 'url': url})

    form = PostForm()

    context = {
        'content': content,
        'url': url,
        'form': form
    }

    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    content = 'Редактировать запись'
    url = f'/posts/{post_id}/edit/'
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()

            return redirect('posts:post_detail', post_id)

        return render(request, 'contact.html', {'content': content, 'form': form, 'url': url, 'is_edit': True})

    form = PostForm(instance=post)

    context = {
        'content': content,
        'url': url,
        'form': form,
        'is_edit': True
    }

    return render(request, 'posts/create_post.html', context)
