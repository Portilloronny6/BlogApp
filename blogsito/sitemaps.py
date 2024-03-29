from django.contrib.sitemaps import Sitemap

from blogsito.models import Post


class PostSitemap(Sitemap):
    change_freq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
