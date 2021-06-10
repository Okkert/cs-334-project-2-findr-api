from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    # ------------------- USERS ------------------- #
    path('register_user/', views.RegisterUser.as_view(), name="register_user"),
    path('login_user/', views.LoginUser.as_view(), name="login_user"),
    path('logout_user/', views.LogoutUser.as_view(), name="logout_user"),
    path('load_user/', views.LoadUser.as_view(), name="load_user"),
    path('update_user/', views.UpdateUser.as_view(), name="update_user"),
    # ------------------- GROUPS ------------------- #
    path('group/', views.Group.as_view(), name="group"),
    path('leave_group/', views.LeaveGroup.as_view(), name="leave_group"),
    path('join_group/', views.JoinGroup.as_view(), name="leave_group"),
    path('load_group_posts/', views.LoadGroupPosts.as_view(), name="load_group_posts"),
    path('load_group_members/', views.LoadGroupMembers.as_view(), name="load_group_members"),
    path('search_groups/', views.SearchGroups.as_view(), name="search_groups"),
    path('promote_member/', views.PromoteMember.as_view(), name="promote_member"),
    path('demote_member/', views.DemoteMember.as_view(), name="demote_member"),
    path('load_join_request/', views.LoadJoinRequest.as_view(), name="load_join_request"),
    path('request_join_group/', views.RequestJoinGroup.as_view(), name="request_join_group"),
    path('accept_join_request/', views.AcceptJoinRequest.as_view(), name="accept_join_request"),
    path('decline_join_request/', views.DeclineJoinRequest.as_view(), name="decline_join_request"),
    # ------------------- POSTS ------------------- #
    path('post/', views.Post.as_view(), name="post"),
    path('like_post/', views.LikePost.as_view(), name="like+post"),
    # ------------------ COMMENT ------------------ #
    path('comment/', views.Comment.as_view(), name="comment"),
    # ------------------ NOTIFICATIONS ------------------ #
    path('notifications/', views.Notification.as_view(), name="note")
]