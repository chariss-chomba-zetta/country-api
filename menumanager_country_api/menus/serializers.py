from rest_framework import serializers

class UpdateRedisSerializer(serializers.Serializer):
    shortCode = serializers.CharField(required=False, default=None)

class RedisOmniServicesSerializer(serializers.Serializer):
    shortCode = serializers.IntegerField()
