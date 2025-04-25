from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseNotFound, Http404

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
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No Post found.")

    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={
            "post": post,
        },
    )
