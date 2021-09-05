from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView

from blog.models import Post


class PostListView2(ListView):
    queryset = Post.published.all()
    context_object_name = "post"
    paginate_by = 3
    template_name = "blog/post/list.html"


class PostListView(View):
    def get(self, request):
        objects_list = Post.objects.all()
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
            "post": posts
        }
        return render(request, "blog/post/list.html", context)


class PostDetailView(View):
    def get(self, request, year, month, day, post_slug):
        post = get_object_or_404(Post,
                                 slug=post_slug,
                                 status="published",
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)

        return render(request, "blog/post/detail.html", {"post": post})
