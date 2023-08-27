# models.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *


@receiver(post_save, sender=Follow)
def update_follower_following_count(sender, instance, **kwargs):

    user1 = User.objects.get(id=instance.follower.id)
    user2 = User.objects.get(id=instance.following.id)

    follower_following_count = user1.following_count
    following_follower_count = user2.follower_count

    if user1:
        instance.follower.following_count = follower_following_count + 1
        instance.follower.save()

    if user2:
        instance.following.follower_count = following_follower_count + 1
        instance.following.save()


@receiver(post_delete, sender=Follow)
def update_follower_following_count_on_delete(sender, instance, **kwargs):
    user1 = instance.follower
    user2 = instance.following

    if user1:
        user1.following_count = user1.following_count - 1
        user1.save()

    if user2:
        user2.follower_count = user2.follower_count - 1
        user2.save()


@receiver(post_save, sender=PostInteraction)
def update_post_interaction(sender, instance, created, **kwargs):
    if created:

        post = instance.post
        interaction_type = instance.interaction_type

        if interaction_type == PostInteraction.COMMENT and instance.interaction_text:
            post.interaction_count += 1
            post.save()
        elif interaction_type == PostInteraction.LIKE:
            post.interaction_count += 1
            post.save()


@receiver([post_save, post_delete], sender=Like)
def update_post_interaction_count(sender, instance, **kwargs):
    post = instance.post
    if post:
        like_count = Like.objects.filter(post=post).count()
        post.interaction_count = like_count
        post.save()


@receiver(post_save, sender=Comment)
def update_post_interaction_on_comment(sender, instance, created, **kwargs):
    if created:
        # Increase the interaction count of the associated post
        post = instance.post
        post.interaction_count += 1
        post.save()


@receiver(post_delete, sender=Comment)
def update_post_interaction_on_comment_delete(sender, instance, **kwargs):
    # Decrease the interaction count of the associated post
    post = instance.post
    post.interaction_count -= 1
    post.save()


@receiver(post_save, sender=CommentReply)
def update_post_interaction_on_reply(sender, instance, created, **kwargs):
    if created:
        # Increase the interaction count of the associated post
        post = instance.comment.post
        post.interaction_count += 1
        post.save()


@receiver(post_delete, sender=CommentReply)
def update_post_interaction_on_reply_delete(sender, instance, **kwargs):
    # Decrease the interaction count of the associated post
    post = instance.comment.post
    post.interaction_count -= 1
    post.save()


@receiver(post_save, sender=PostShare)
def update_shared_post_interaction(sender, instance, created, **kwargs):
    if created:
        instance.original_post.interaction_count += 1
        instance.original_post.save()


@receiver(post_delete, sender=PostShare)
def reduce_shared_post_interaction(sender, instance, **kwargs):
    instance.original_post.interaction_count -= 1
    instance.original_post.save()
