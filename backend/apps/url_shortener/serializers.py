from rest_framework import serializers
from .models import Url


class BaseUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url

class UrlCreateSerializer(BaseUrlSerializer):
    def create(self, validated_data):
        short_code = Url.create_short_code()
        return Url.objects.create(
            original_url=validated_data['original_url'],
            short_code=short_code
        )

    class Meta(BaseUrlSerializer.Meta):
        fields = ('original_url',)


class UrlSerializer(BaseUrlSerializer):
    short_url = serializers.SerializerMethodField()
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return f"{request.scheme}://{request.get_host()}/r/{obj.short_code}"

        return f"/r/{obj.short_code}"

    class Meta(BaseUrlSerializer.Meta):
        fields = ('original_url', 'short_code', 'short_url', 'created_at',)