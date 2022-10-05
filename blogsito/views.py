from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views import View

from blogsito.forms import EmailPostForm
from blogsito.models import Post


class PostListView(View):

    def get(self, request):
        posts = Post.published.all()
        paginator = Paginator(posts, 3)  # 3 posts in each page_number
        page_number = request.GET.get('page_number')
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            # if page_number is not an integer deliver the first page_number
            posts = paginator.page(1)
        except EmptyPage:
            # If page_number is out of range deliver last page_number of results
            posts = paginator.page(paginator.num_pages)
        context = {
            'posts': posts,
            'page_number': page_number,
        }
        return render(request, 'blogsito/list.html', context=context)


class PostDetailView(View):

    def get(self, request, year, month, day, slug):
        post = get_object_or_404(
            Post, slug=slug, status=Post.Status.PUBLISHED,
            publish__year=year, publish__month=month, publish__day=day
        )
        context = {
            'post': post,
        }
        return render(request, 'blogsito/detail.html', context=context)


class PostShareView(View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        form = EmailPostForm()
        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'blogsito/share.html', context=context)

    def post(self, request, post_id):
        # Retrieve post by id
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        form = EmailPostForm(request.POST)
        sent = False

        if form.is_valid():
            # Form fields passed validation
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {data['name']}\n's comments: {data['comments']}"
            send_mail(subject, message, 'admin@blogsito.com', [data['to']])
            sent = True

        context = {
            'post': post,
            'form': form,
            'sent': sent
        }

        return render(request, 'blogsito/share.html', context=context)
