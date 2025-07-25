from django.contrib import admin
from .models import Profile, Friend

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user__username", "nick_name")
    search_fields = ("user__username",)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ["pk", "sender", "receiver", "status"]
