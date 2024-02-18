from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ["owner"]
    
    def create(self, validated_data):
        validated_data["owner"] = self.context.get("request").user
        return super().create(validated_data)
