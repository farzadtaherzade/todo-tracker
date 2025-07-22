from django.urls import path
from .views import RetrieveUpdateProfileView

urlpatterns = [
    path("", RetrieveUpdateProfileView.as_view(),
         name="retrieve-update-profile"),
]
