from django.urls import path

from blogsito.feeds import LatestPostsFeed
from blogsito.views import *

app_name = 'blogsito'

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('tag/<slug:tag_slug>', PostListView.as_view(), name='posts_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/', PostShareView.as_view(), name='post_share'),
    path('<int:post_id>/comment/', PostCommentView.as_view(), name='post_comment'),
    path('feed/', LatestPostsFeed(), name='latest_posts_feed'),
    path('search/', PostsSearchView.as_view(), name='posts_search'),
]
