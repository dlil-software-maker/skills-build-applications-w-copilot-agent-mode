from bson import ObjectId
from rest_framework import serializers
from .models import Team


def _normalize_objectid(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, dict):
        return {k: _normalize_objectid(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_objectid(v) for v in value]
    return value


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk', read_only=True)

    class Meta:
        model = Team
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return _normalize_objectid(representation)
