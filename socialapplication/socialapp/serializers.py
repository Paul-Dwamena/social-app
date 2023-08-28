from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializer import UserSerializer
from rest_framework.serializers import CurrentUserDefault





class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'firstname', 'lastname',)  

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'



class PostInteractionTypeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = UserSerializer()

    class Meta:
        model = PostInteraction
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
   

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = UserSerializer()

    class Meta:
        model = Like
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupMembershipSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    user = UserSerializer()

    class Meta:
        model = GroupMembership
        fields = '__all__'


# class CommentReplySerializer(serializers.ModelSerializer):
#     comment = serializers.PrimaryKeyRelatedField(
#         queryset=Comment.objects.all())
#     user = UserSerializer()

#     class Meta:
#         model = CommentReply
#         fields = '__all__'



class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Post
        fields = '__all__'


class PostShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostShare
        fields = '__all__'

class FollowsSerializer(serializers.Serializer):
    following_id = serializers.IntegerField()  # Add following_id field


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'group_name', 'group_description',)  


class JoinLeaveGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()  


class CreatePostSerializer(serializers.ModelSerializer):
    tag_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id', 'post_text', 'post_image_url','post_video_url','audience_type','tag_id','user_id') 

    

class PostCommentSerializer(serializers.Serializer):
    comment_text = serializers.CharField()

    class Meta:
        fields = ['comment_text']




class CreatePostShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostShare
        fields = ('id', 'original_post') 

    

class PostShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostShare
        fields = '__all__'



class CreateCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = ('id', 'reply_text') 
