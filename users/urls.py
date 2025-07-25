from django.urls import path
from .views import (RetrieveUpdateProfileView,
                    SendAndListFriendRequests,
                    accept_or_reject_friend_request,
                    ListRreceivedFriendRequest,
                    saerch_username,
                    SetUsernameView
                    )

urlpatterns = [
    path("", RetrieveUpdateProfileView.as_view(),
         name="retrieve-update-profile"),
    path("username/", SetUsernameView.as_view(), name="set-username"),
    path("friend/request/", SendAndListFriendRequests.as_view(),
         name="send-list-friend-request"),
    path("friend/answer/<int:friend_pk>/", accept_or_reject_friend_request,
         name="answer-friend-request"),
    path("friend/received/", ListRreceivedFriendRequest.as_view(),
         name="list-received-friend-request"),
    path("friend/find/<str:username>", saerch_username, name="find-friend"),
]
