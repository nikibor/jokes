from rest_framework import serializers


class JokeTextSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=False,
        allow_null=False
    )
    text = serializers.CharField(
        max_length=500,
        allow_null=False,
        required=True
    )


class JokeListSerializer(serializers.Serializer):
    jokes = serializers.ListField(
        child=JokeTextSerializer(),
        allow_null=False,
        required=True
    )
