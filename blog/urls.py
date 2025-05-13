from django.urls import path

from .feeds import LatestPostsFeed

from . import views

app_name = "blog"
urlpatterns = [
    path(
        route="",
        view=views.post_list,
        name="post-list",
    ),
    path(
        route="tag/<slug:tag_slug>/",
        view=views.post_list,
        name="post-list-by-tag",
    ),
    # path(
    #     route="",
    #     view=views.PostListView.as_view(),
    #     name="post-list",
    # ),
    path(
        route="<int:year>/<int:month>/<int:day>/<slug:post>/",
        view=views.post_detail,
        name="post_detail",
    ),
    path(
        route="<int:post_id>/share/",
        view=views.post_share,
        name="share-post",
    ),
    path(
        route="<int:post_id>/comment/",
        view=views.post_comment,
        name="comment-post",
    ),
    path("feed/", LatestPostsFeed(), name="post-feed"),
]
