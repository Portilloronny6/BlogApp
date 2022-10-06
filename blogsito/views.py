from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views import View
from taggit.models import Tag

from blogsito.forms import EmailPostForm, CommentForm
from blogsito.models import Post


class PostListView(View):

    def get(self, request, tag_slug=None):
        posts = Post.published.all()
        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[tag])

        paginator = Paginator(posts, 3)  # 3 posts in each page_number
        page_number = request.GET.get('page')

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
            'tag': tag,
        }
        return render(request, 'blogsito/list.html', context=context)


class PostDetailView(View):

    def get(self, request, year, month, day, slug):
        post = get_object_or_404(
            Post, slug=slug, status=Post.Status.PUBLISHED,
            publish__year=year, publish__month=month, publish__day=day
        )
        comments = post.comments.filter(active=True)
        form = CommentForm()

        # List of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

        context = {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts,
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


class PostCommentView(View):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        form = CommentForm(request.POST)
        comment = None

        if form.is_valid():
            # Create Comment object but don't save to database yet
            comment = form.save(commit=False)
            # Assign the current post to the comment
            comment.post = post
            # Save the comment to the database
            comment.save()

        context = {
            'post': post,
            'comment': comment,
            'form': form,
        }
        return render(request, 'blogsito/comment.html', context=context)
