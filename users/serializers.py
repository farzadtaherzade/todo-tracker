from .models import Profile, Friend
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = ("id",)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "avatar", "nick_name", "bio", "user")
        read_only_fields = ("id", "user")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"
        read_only_fields = ("sender", "status", "created_at")


class FriendSerializerAnswer(serializers.Serializer):
    answer = serializers.BooleanField()


class SetUsernameSerializer(serializers.Serializer):
    username = serializers.SlugField(write_only=True)
