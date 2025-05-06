from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.http import HttpRequest

from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 2
    context_object_name = "posts"
    template_name = "blog/post/list.html"


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


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url)
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[
                    cd["to"],
                ],
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        template_name="blog/post/share.html",
        context={
            "post": post,
            "form": form,
            "sent": sent,
        },
    )
