from django.db import models

# Create your models here.
from django.db import models
from authentication.models import User
from django.db.models.signals import post_save
import datetime
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.tag_name


class Post(models.Model):

    PUBLIC = "public"
    PRIVATE = "private"
    GROUP = "group"

    AUDIENCE_CHOICES = (
        (PUBLIC, "public"),
        (PRIVATE, "private"),
        (GROUP, "group"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post_text = models.TextField(blank=True)
    post_image_url = models.CharField(max_length=200, blank=True)
    post_video_url = models.CharField(max_length=200, blank=True)
    interaction_count = models.IntegerField(default=0, blank=True)
    audience_type = models.CharField(
        max_length=10,
        choices=AUDIENCE_CHOICES,
        default=PUBLIC,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostInteraction(models.Model):
    LIKE = "like"
    COMMENT = "comment"
    SHARE="share"

    INTERACTION_CHOICES = (
        (LIKE, "Like"),
        (COMMENT, "Comment"),
        (SHARE,"share")
    )

    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_CHOICES,
        default=LIKE,
    )
    interaction_text = models.TextField(blank=True)
    interaction_media = models.TextField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], condition=models.Q(
                interaction_type='like'), name='unique_like_interaction')
        ]

    def validate_unique(self, exclude=None):
        if self.interaction_type == 'like':
            queryset = PostInteraction.objects.filter(
                post=self.post, user=self.user, interaction_type='like'
            )
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            if queryset.exists():
                raise ValidationError(
                    {'interaction_type': 'A user can only like a post once.'}
                )
        super().validate_unique(exclude)

    def __str__(self):
        return self.get_interaction_type_display()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='followers_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower} -> {self.following}"

   


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_description = models.TextField(blank=True)
    group_users_count = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostShare(models.Model):
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shared_by} shared {self.original_post}"

    class Meta:
        unique_together = ('shared_by', 'original_post')