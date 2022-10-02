from django.shortcuts import render, get_object_or_404
from django.views import View

from blogsito.models import Post


class PostListView(View):

    def get(self, request):
        posts = Post.published.all()
        context = {
            'posts': posts,
        }
        return render(request, 'blogsito/list.html', context=context)


class PostDetailView(View):

    def get(self, request, year, month, day, slug):
        post = get_object_or_404(
            Post, slug=slug, status='published', publish__year=year,
            publish__month=month, publish__day=day
        )
        context = {
            'post': post,
        }
        return render(request, 'blogsito/detail.html', context=context)
