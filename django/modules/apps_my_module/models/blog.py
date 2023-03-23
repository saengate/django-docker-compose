from django.db import models

from modules.apps_my_module.models.comment import Comment


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    comments = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='blog',
        null=True,
    )

    def __str__(self):
        return self.name
