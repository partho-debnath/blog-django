from django.conf import settings
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                status=Post.Status.PUBLISHED,
            )
        )


class Post(models.Model):

    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.TextField(
        max_length=2,
        choices=Status.choices,
        db_default=Status.DRAFT,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(
                fields=["-publish"],
            ),
        ]
        default_manager_name = "published"
