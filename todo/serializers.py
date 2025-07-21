from .models import Todo
from rest_framework.serializers import ModelSerializer


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
        read_only_fields = ("owner", "created_at", "updated_at")
