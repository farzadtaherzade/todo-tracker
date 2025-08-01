from .models import Profile, Friend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from .serializers import ProfileSerializer, FriendSerializer, FriendSerializerAnswer, UserSerializer, SetUsernameSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class RetrieveUpdateProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get(self, request):
        profile = self.get_object()
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = self.get_object()
        serializer = self.serializer_class(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        profile = self.get_object()
        serializer = self.serializer_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendAndListFriendRequests(generics.ListCreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def perform_create(self, serializer):
        receiver = self.request.data.get("receiver")

        if int(receiver) == self.request.user.id:
            raise serializers.ValidationError(
                "You can't send friend request to yourself")

        if Friend.objects.filter(receiver_id=int(receiver), sender=self.request.user).exists():
            raise serializers.ValidationError("Friend alread exists")

        return serializer.save(sender=self.request.user)

    def get_queryset(self):
        return Friend.objects.filter(sender=self.request.user)


@api_view(["POST", "GET"])
def accept_or_reject_friend_request(request, friend_pk):
    try:
        friend = Friend.objects.get(pk=friend_pk, receiver=request.user)
    except Friend.DoesNotExist:
        return Response(data={"message": "not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        answer_serializer = FriendSerializerAnswer(data=request.data)
        if answer_serializer.is_valid():
            new_status = 2 if answer_serializer.validated_data.get(
                "answer") else 3
            friend.status = new_status
            friend.save()
            serializer = FriendSerializer(friend)
            return Response(serializer.data)
        return Response(answer_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        serializer = FriendSerializer(friend)
        return Response(serializer.data)


class ListRreceivedFriendRequest(generics.ListAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)


@api_view(["GET"])
def saerch_username(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(data={"message": "User Does Not Found"}, status=status.HTTP_404_NOT_FOUND)


class SetUsernameView(generics.GenericAPIView):
    queryset = User
    serializer_class = SetUsernameSerializer

    def post(self, request):
        serializer = SetUsernameSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]

            if not User.objects.filter(username=username).exists():
                request.user.username = username
                request.user.save()

                return Response({"message": "Username set successfully"}, status=status.HTTP_200_OK)

            return Response({"message": "Username already in use."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"username": request.user.username})
