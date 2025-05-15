from django.shortcuts import render, get_object_or_404

from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)
from django.views.generic import ListView
from django.core.mail import send_mail
from django.http import HttpRequest
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage,
)


from taggit.models import Tag

from .models import Post
from .forms import (
    EmailPostForm,
    CommentModelForm,
    SearchForm,
)


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # pagination with 2 posts per page
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request=request,
        template_name="blog/post/list.html",
        context={
            "posts": posts,
            "tag": tag,
        },
    )


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
    similar_posts = (
        Post.published.exclude(id=post.id)
        .filter(
            tags__id__in=post.tags.values_list(
                "id",
                flat=True,
            ),
        )
        .alias(tag_count=Count("tags", distinct=True))
        .order_by("-tag_count", "-publish")[:4]
    )
    comment_form = CommentModelForm()
    comments = post.comments.filter(active=True)
    return render(
        request=request,
        template_name="blog/post/detail.html",
        context={
            "post": post,
            "form": comment_form,
            "comments": comments,
            "similar_posts": similar_posts,
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


@require_POST
def post_comment(request, post_id):
    post_obj = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        id=post_id,
    )
    comment_form = CommentModelForm(data=request.POST)
    comment_obj = None
    if comment_form.is_valid():
        comment_obj = comment_form.save(commit=False)
        comment_obj.post = post_obj
        comment_obj.save()

    return render(
        request=request,
        template_name="blog/post/comment.html",
        context={
            "form": comment_form,
            "post": post_obj,
            "comment": comment_obj,
        },
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", "body")
            search_query = SearchQuery(query)
            results = (
                Post.published.alias(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                )
                .filter(search=search_query)
                .order_by("-rank")
            )
    return render(
        request=request,
        template_name="blog/post/search.html",
        context={
            "form": form,
            "query": query,
            "results": results,
        },
    )
