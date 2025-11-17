from rest_framework import serializers

class CategoryDTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
