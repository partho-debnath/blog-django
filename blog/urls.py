from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path(route="", view=views.PostListView.as_view(), name="post-list"),
    path(
        route="<int:year>/<int:month>/<int:day>/<slug:post>/",
        view=views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", views.post_share, name="share-post"),
    path("<int:post_id>/comment/", views.post_comment, name="comment-post"),
]
