from rest_framework import serializers
from .models import Url


class BaseUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url

class UrlCreateSerializer(BaseUrlSerializer):
    url = serializers.URLField(source='original_url')
    
    def create(self, validated_data):
        short_code = Url.create_short_code()
        return Url.objects.create(
            original_url=validated_data['original_url'],
            short_code=short_code
        )

    class Meta(BaseUrlSerializer.Meta):
        fields = ('url',)


class UrlSerializer(BaseUrlSerializer):
    short_url = serializers.SerializerMethodField()
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return f"{request.scheme}://{request.get_host()}/api/urls/url/{obj.short_code}"

        return f"/api/urls/url/{obj.short_code}"

    class Meta(BaseUrlSerializer.Meta):
        fields = ('original_url', 'short_code', 'short_url', 'created_at',)