from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "author",
        "publish",
        "status",
    ]
    list_filter = [
        "status",
        "created",
        "publish",
        "author",
    ]
    search_fields = [
        "title",
        "body",
        "author__email",
    ]
    search_help_text = "Search Post based on title or body or author-email"
    prepopulated_fields = {
        "slug": [
            "title",
        ],
    }
    raw_id_fields = [
        "author",
    ]
    ordering = [
        "publish",
        "status",
    ]
    date_hierarchy = "publish"
    show_facets = admin.ShowFacets.ALWAYS
    # autocomplete_fields = [
    #     "author",
    # ]


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
        "post",
        "created",
        "active",
    ]
    list_filter = [
        "active",
        "created",
        "updated",
    ]
    search_fields = [
        "name",
        "email",
        "body",
    ]
