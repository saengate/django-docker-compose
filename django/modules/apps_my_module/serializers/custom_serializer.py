from rest_framework import serializers


class CustomSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=False,
        max_length=10,
        min_length=3,
    )
    custom_value = serializers.SerializerMethodField()

    def validate_name(self, value):
        return value

    def get_custom_value(self, data):
        return 9 + 9

    def to_internal_value(self, data):
        name = data.get('name', '')
        if name:
            data['name'] = 'otra cosa'
        return super().to_internal_value(data)
