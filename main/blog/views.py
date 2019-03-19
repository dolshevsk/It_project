from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Post, Tag
from .utils import ObjectDetailMixin
from .forms import TagForm, PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query ))
    else:
        posts = Post.objects.all()
    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''
    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }
    return render(request, 'blog/index.html', context)


class PostDetail(ObjectDetailMixin,View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_create.html', context={'form':form})
        
    
    def post(self, request):
        bound_form = PostForm(request.POST)
        
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'blog/post_create.html', context={'form': bound_form})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags':tags})

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request):
        form = TagForm()
        return render(request, 'blog/tag_create.html', context={'form':form})

    def post(self, request):
        bound_form = TagForm(request.POST)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/tag_create.html', context={'form': bound_form})

class TagUpdate(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(instance=tag)
        return render(request, 'blog/tag_update.html', context={'form': bound_form, 'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(request.POST, instance=tag)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/tag_update.html', context={'form': bound_form, 'tag': tag})

class PostUpdate(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(instance=post)
        return render(request, 'blog/post_update.html', context={'form': bound_form, 'post': post})

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(request.POST, instance=post)

        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'blog/post_update.html', context={'form': bound_form, 'post': post})

class TagDelete(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        return render(request, 'blog/tag_delete.html', context={'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        tag.delete()
        return redirect(reverse('tags_list_url'))

class PostDelete(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        return render(request, 'blog/post_delete.html', context={'post': post})

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        post.delete()
        return redirect(reverse('post_list_url'))