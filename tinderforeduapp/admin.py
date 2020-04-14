from django.contrib import admin
from .models import *
from chat.models import Savechat
admin.site.register(Profile)
admin.site.register(UserInfo)
admin.site.register(Savechat)
admin.site.register(Comment)
admin.site.register(ProfilePic)
admin.site.register(MatchContainer)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
# Register your models here.
