from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest

from .models import Post


def post_list(request: HttpRequest):
    posts = Post.published.all()
    return render(
        request=request,
        template_name="blog/post/list.html",
        context={
            "posts": posts,
        },
    )


def post_detail(request: HttpRequest, id: int):
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED,
    )
    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={
            "post": post,
        },
    )
