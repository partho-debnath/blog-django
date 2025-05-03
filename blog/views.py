from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpRequest

from .models import Post


def post_list(request: HttpRequest):

    post_list = Post.published.all()
    paginator = Paginator(object_list=post_list, per_page=2)

    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="blog/post/list.html",
        context={
            "posts": posts,
        },
    )


def post_detail(
    request: HttpRequest,
    year: int,
    month: int,
    day: int,
    post: str,
):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED,
    )
    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={
            "post": post,
        },
    )
