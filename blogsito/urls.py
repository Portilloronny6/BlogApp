from django.urls import path

from blogsito.views import *

app_name = 'blogsito'

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/', PostShareView.as_view(), name='post_share')
]
