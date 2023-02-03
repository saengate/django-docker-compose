from apps_my_module.models.comments import Comments


class CommentFactory:

    def __init__(
        self,
        **kwargs,
    ):
        self.data = {
            'comment': 'Blog Test bla bla bla',
        }
        self.data.update(**kwargs)

    def create(self) -> Comments:
        return Comments.objects.create(**self.data)
