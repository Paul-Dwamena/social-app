from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_text', 'created_at')


@admin.register(PostInteraction)
class PostInteractionTypeAdmin(admin.ModelAdmin):
    list_display = ('interaction_type', 'post', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_text', 'created_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_description', 'created_at','group_users_count')


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'joined_at')


@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'reply_text', 'created_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_text', 'is_read', 'created_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)


@admin.register(PostShare)
class PostShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('shared_by__username', 'post__post_text')
