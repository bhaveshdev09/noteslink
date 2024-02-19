from rest_framework import serializers
from notes.models import Note
from users.models import CustomUser
from rest_framework.exceptions import PermissionDenied


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ["owner"]

    def create(self, validated_data):
        validated_data["owner"] = self.context.get("request").user
        return super().create(validated_data)


class ShareNoteSerializer(serializers.ModelSerializer):
    note = serializers.PrimaryKeyRelatedField(
        queryset=Note.objects.all(), write_only=True
    )

    users = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True, write_only=True, required=True
    )

    class Meta:
        model = Note
        fields = ["note", "users"]

    def validate_users(self, value):
        if not value:
            raise serializers.ValidationError("At least one user is required.")
        return value

    def update(self, instance, validated_data, **kwargs):
        user_list = validated_data.get("users")
        user_list = set(user_list)
        auth_user = kwargs.get("auth_user")
        if auth_user != instance.owner:
            raise PermissionDenied(
                detail="You do not have permission to share this note"
            )
        # if note owner in users provided then discard owner (as owner has access to note) from list
        if instance.owner in user_list:
            user_list.discard(instance.owner)

        # Add user in shared users
        instance.shared_with.add(*list(user_list))
        return instance
