from rest_framework import serializers

from modules.apps_my_module.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def validate_name(self, value):
        return value + '0001'

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, instance):
        instance.name = 'bababababa'
        return super().to_representation(instance)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
