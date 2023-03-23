from modules.apps_my_module.models.comment import Comment


class CommentFactory:

    def __init__(
        self,
        **kwargs,
    ):
        self.data = {
            'comment': 'Blog Test bla bla bla',
        }
        self.data.update(**kwargs)

    def create(self) -> Comment:
        return Comment.objects.create(**self.data)
