from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.views import *

from .views import *


router = DefaultRouter()
router.register(r'tags', TagViewSet)



urlpatterns = [
     path('follow', FollowView.as_view(), name="follow"),
     path('unfollow', UnfollowView.as_view(), name="unfollow"),
     path('following-followers-list', ListFollowersFollowing.as_view(),
          name="following-followers-list"),

     path('post/like_unlike_post/<int:post_id>/',
          like_unlike_post, name="like_unlike_post"),
     path('post/get_posts', get_posts, name="get_posts"),
     path('post/create_post', PostCreateView.as_view(), name="create_post"),
     path('post/edit-post/<int:post_id>', EditPostView.as_view(), name='edit-post'),
     path('post/delete-post/<int:post_id>', delete_post, name='delete-post'),
  
  
     path('comments/<int:comment_id>', delete_comment, name='delete_comment'),
     path('comments/<int:comment_id>/replies',
          get_comment_replies, name='get_comment_replies'),
     path('comments/<int:comment_id>/replies',
          create_comment_reply, name='create_comment_reply'),
     path('comments/<int:comment_id>/replies/<int:reply_id>',
          delete_comment_reply, name='delete_comment_reply'),
     path('comments/create-comment-reply/<int:comment_id>/', CreateCommentReplyView.as_view(), name='create-comment-reply'),


     path('posts/<int:post_id>/comments',get_comments_for_post, name='get_comments_for_post'),
     path('posts/<int:post_id>/create-comment', CreatePostCommentView.as_view(), name='create_comment'),
     path('posts/shared-posts', get_shared_posts, name='get_shared_posts'),
     path('posts/shared-posts/<int:post_share_id>', delete_shared_post, name='delete_shared_post'),
     path('posts/create-shared-post/', CreateSharedPostView.as_view(), name='create-shared-post'),
          
    
     path('group/create-group', GroupCreateView.as_view(), name="create_group"),
     path('group/group_details', GroupDetailsView.as_view(), name="group_details"),
     path('group/join-group', JoinGroupView.as_view(), name="join-group"),
     path('group/leave-group', LeaveGroupView.as_view(), name="join-leave_group"),
     path('group/edit-delete-group/<int:group_id>/', EditDeleteGroupView.as_view(), name="edit_delete_group"),
     path('search/', SearchApiView.as_view(), name='search'),
     path('post/trending-popular-posts/', TrendingAndPopularPostsView.as_view(), name='trending-popular-posts'),
     path('', include(router.urls))
]
