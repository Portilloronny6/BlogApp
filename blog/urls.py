from django.urls import path
from blog.views import PostListView, PostDetailView, PostShareView
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    # post views
    path('', PostListView.as_view(), name="post_list"),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name="post_list_by_tag"),
    path('<int:post_id>/share/', PostShareView.as_view(), name="post_share"),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', PostDetailView.as_view(), name="post_detail"),
    path('feed/', LatestPostsFeed(), name="post_feed"),
]
