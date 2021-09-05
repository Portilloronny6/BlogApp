from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán antes de entrar al detalle del post
    list_display = ("title", "slug", "author", "publish", "status")

    # A partir de que columnas se podrá filtrar los posts
    list_filter = ("slug", "created", "publish", "author")

    # Columnas que podran ser buscadas
    search_fields = ("title", "body")

    # Cuando se escriba el titulo, se llenara el slug automaticamente
    prepopulated_fields = {"slug": ("title",)}

    # aparecera una lupa para hacer busquedas a partir de este campo
    raw_id_fields = ("author",)

    # fechas para mostrar los posts con cierta jerarquia
    date_hierarchy = "publish"

    # de que manera se podran ordenar los posts
    ordering = ("status", "publish")
