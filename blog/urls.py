from django.urls import path

from blog.views import PostListView, PostDetailView, PostListView2

app_name = "blog"

urlpatterns = [
    # post views
    path('', PostListView.as_view(), name="post_list"),
    # path('', PostListView2.as_view(), name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', PostDetailView.as_view(), name="post_detail"),
]
