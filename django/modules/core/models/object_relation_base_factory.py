from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldError


def object_relation_base_factory(
    prefix=None,
    prefix_verbose=None,
    add_related_name=False,
    limit_content_type_choices_to=None,
    is_required=False,
):
    """
    Returns a mixin class for generic foreign keys using
    "Content type - object ID" with dynamic field names.
    This function is just a class generator.
    Parameters:
    prefix:           a prefix, which is added in front of
                      the fields
    prefix_verbose:   a verbose name of the prefix, used to
                      generate a title for the field column
                      of the content object in the Admin
    add_related_name: a boolean value indicating, that a
                      related name for the generated content
                      type foreign key should be added. This
                      value should be true, if you use more
                      than one ObjectRelationMixin in your
                      model.
    The model fields are created using this naming scheme:
        <<prefix>>_content_type
        <<prefix>>_object_id
        <<prefix>>_content_object
    """
    p = ''
    if prefix:
        p = f'{prefix}_'

    prefix_verbose = prefix_verbose or _('Related object')
    limit_content_type_choices_to = limit_content_type_choices_to or {}

    content_type_field = f'{p}content_type'
    object_id_field = f'{p}object_id'
    content_object_field = f'{p}content_object'

    class TheClass(models.Model):
        class Meta:
            abstract = True

    if add_related_name:
        if not prefix:
            raise FieldError('if add_related_name is set to '
                             'True, a prefix must be given')
        related_name = prefix
    else:
        related_name = None

    optional = not is_required

    ct_verbose_name = _(f"{prefix_verbose}'s type(model)")  # NOQA

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=ct_verbose_name,
        related_name=related_name,
        blank=optional,
        null=optional,
        help_text=_('Please select the type (model) '
                    'for the relation, you want to build.'),
        limit_choices_to=limit_content_type_choices_to,
        on_delete=models.CASCADE)

    fk_verbose_name = prefix_verbose

    object_id = models.CharField(
        fk_verbose_name,
        blank=optional,
        null=False,
        help_text=_('Please enter the ID of the related object.'),
        max_length=255,
        default='')  # for migrations

    content_object = GenericForeignKey(
        ct_field=content_type_field,
        fk_field=object_id_field)

    TheClass.add_to_class(content_type_field, content_type)
    TheClass.add_to_class(object_id_field, object_id)
    TheClass.add_to_class(content_object_field,
                          content_object)

    return TheClass
