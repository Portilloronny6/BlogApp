from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views import View
from taggit.models import Tag
from blog.forms import EmailPostForm, CommentForm
from blog.models import Post
from django.db.models import Count


class PostListView(View):
    def get(self, request, tag_slug=None):
        objects_list = Post.objects.all()
        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            objects_list = objects_list.filter(tags__in=[tag])

        paginator = Paginator(objects_list, 3)  # 3 posts in each page
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results
            posts = paginator.page(paginator.num_pages)

        context = {
            "page": page,
            "post": posts,
            "tag": tag
        }
        return render(request, "blog/post/list.html", context)


class PostDetailView(View):
    def get(self, request, year, month, day, post_slug):
        post = get_object_or_404(Post, slug=post_slug, status="published",
                                 publish__year=year, publish__month=month,
                                 publish__day=day)

        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by("-same_tags", "-publish")[:4]
        context = {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
            "similar_posts": similar_posts,
        }
        return render(request, "blog/post/detail.html", context)

    def post(self, request, year, month, day, post_slug):
        post = get_object_or_404(Post, slug=post_slug, status="published",
                                 publish__year=year, publish__month=month,
                                 publish__day=day)

        # A comment was posted
        comments = post.comments.filter(active=True)
        new_comment = None
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

        context = {
            "post": post,
            "new_comment": new_comment,
            "comments": comments,
            "comment_form": comment_form,
        }
        return render(request, "blog/post/detail.html", context)


class PostShareView(View):

    def get(self, request, post_id):
        looking_post = get_object_or_404(Post, id=post_id, status="published")
        form = EmailPostForm()
        context = {
            "post": looking_post,
            "form": form,
        }
        return render(request, "blog/post/share.html", context)

    def post(self, request, post_id):
        looking_post = get_object_or_404(Post, id=post_id, status="published")
        form = EmailPostForm(request.POST)
        sent = False
        if form.is_valid():
            # Form fields passed validation
            clean_data = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(looking_post.get_absolute_url())
            subject = f"{clean_data['name']} recommends you read {looking_post.title}"
            message = f"Read {looking_post.title} at {post_url}\n\n" \
                      f"{clean_data['name']}'s comments: " \
                      f"{clean_data['comments']}"
            send_mail(subject, message, "admin@myblog.com", [clean_data['to']])
            sent = True
        else:
            form = EmailPostForm()

        context = {
            'post': looking_post,
            'form': form,
            'sent': sent
        }
        return render(request, "blog/post/share.html", context)
