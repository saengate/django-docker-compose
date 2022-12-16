from rest_framework import serializers

from apps_my_module.models import Entry
from apps_my_module.serializers.blog_serializer import BlogSerializer
from apps_my_module.serializers.author_serializer import AuthorSerializer


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


class ReadEntrySerializer(EntrySerializer):
    blog = BlogSerializer()
    authors = AuthorSerializer(many=True)
