from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


@register.simple_tag
def total_published_post() -> int:
    return Post.published.count()


@register.inclusion_tag(filename="blog/post/latest_posts.html")
def show_latest_published_post(count: int = 5):
    latest_posts = Post.published.all()[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_post(count: int = 5):
    return Post.published.alias(
        total_comments=Count("comments"),
    ).order_by(
        "-total_comments"
    )[:count]
