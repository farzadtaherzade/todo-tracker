from .models import Profile, Friend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import ProfileSerializer, FriendSerializer, FriendSerializerAnswer, UserSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


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
            return serializer.ValidateError("You can't send friend request to yourself")

        if Friend.objects.filter(receiver_id=receiver, sender=self.request.user).exists():
            return serializer.ValidateError("Friend alread exists")

    def get_queryset(self):
        return Friend.objects.filter(sender=self.request.user)


@api_view(["POST"])
def accept_or_reject_friend_request(request, friend_pk):
    try:
        friend = Friend.objects.get(pk=friend_pk, receiver=request.user)
    except Friend.DoesNotExist:
        return Response(data={"message": "not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FriendSerializerAnswer(data=request.data)
    if serializer.is_valid:
        if serializer.answer == True:
            friend.status = 2
        else:
            friend.status = 3
        friend.save()

        friend_serializer = FriendSerializer(friend)
        return Response(data={"friend_request": friend_serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


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
