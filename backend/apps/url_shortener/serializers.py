from rest_framework import serializers
from .models import Url


class UrlCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('original_url',)
    
    def create(self, validated_data):
        short_code = Url.create_short_code()
        return Url.objects.create(
            original_url=validated_data['original_url'],
            short_code=short_code
        )


class UrlSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Url
        fields = ('original_url', 'short_code', 'short_url', 'created_at',)
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return f"{request.scheme}://{request.get_host()}/r/{obj.short_code}"

        return f"/r/{obj.short_code}"