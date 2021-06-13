from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from . import groups, posts, comments, auth, user, notes, models
from .auth import get_request_token
from .utils.toolbox import gen_response
from .utils import response_constants as resp

# CONSTANT
invalid_response = Response(status=400, data={"reason": "Invalid response"})
invalid_token = Response(status=401, data={"reason": "Invalid token"})


# import user
# Create your views here.


def index(request):
    return render(request, 'index.html')


def authentic_token(request):
    token = get_request_token(request.headers)
    if token is None:
        return False
    auth_response = auth.confirm_token(token)
    token_valid = auth_response.status_code == resp.OK
    return token_valid


# ------------------- USERS ------------------- #
class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.query_params["username"]
            email = request.query_params["email"]
            # TODO: Asynchronous encryption time
            password = request.query_params["password"]
        except KeyError:
            return invalid_response
        return auth.register(username, email, password)


class LoginUser(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = None
            if 'username' in request.query_params:
                 username = request.query_params["username"]
            email = None
            if 'email' in request.query_params:
                email = request.query_params["email"]
            # TODO: Asynchronous encryption time
            password = request.query_params["password"]
            remember = request.query_params["remember"]
        except KeyError:
            return invalid_response
        return auth.login(username, email, password, remember)


class LogoutUser(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # We don't use the standard token checking here, because the token is also the input
            token = get_request_token(request.headers)
        except KeyError:
            return invalid_response
        return auth.logout(token)


class LoadUser(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
        except KeyError:
            return invalid_response
        return user.load_user(user_id=user_id)


class SearchUser(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
            search_term = request.query_params['username']
        except KeyError:
            return invalid_response
        return user.search_user(search_term, user_id)


class UpdateUser(APIView):
    def put(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
            user_info = {
                "user_id": user_id
            }
            if 'username' in request.query_params:
                username = request.query_params['username']
                user_info['username'] = username
            if 'email' in request.query_params:
                email = request.query_params['email']
                user_info['email'] = email
            if 'bio' in request.query_params:
                bio = request.query_params['bio']
                user_info['bio'] = bio
            if 'password' in request.query_params:
                password = request.query_params['password']
                user_info['password'] = password

        except KeyError:
            return invalid_response
        return user.update_user_details(user_info)


class DeleteUser(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
        except KeyError:
            return invalid_response
        return user.delete_user(user_id)


class LoadFeed(APIView):
    def get(self, request, *args, **kwargs):
        filter_params = {
            "type": "Time"
        }
        try:
            filter_type = request.query_params['type']
            user_id = request.query_params['userId']

            if filter_type == "Time":
                filter_params = {
                    "type": "Time",
                    "userId": user_id
                }

            elif filter_type == "Location":
                location = request.query_params["location"]
                try:
                    distance = request.query_params["distance"]
                except KeyError:
                    distance = 10

                filter_params = {
                    "type": "Location",
                    "userId": user_id,
                    "location": location,
                    "distance": distance
                }

            elif filter_type == "Category":
                category = request.query_params["category"]
                filter_params = {
                    "type": "Category",
                    "userId": user_id,
                    "category": category
                }

            elif filter_type == "User":
                username = request.query_params["username"]
                filter_params = {
                    "type": "User",
                    "userId": user_id,
                    "username": username
                }
            elif filter_type == "Group":
                group_id = request.query_params["groupId"]
                filter_params = {
                    "type": "Group",
                    "userId": user_id,
                    "groupId": group_id
                }

        except KeyError:
            return invalid_response

        return posts.load_feed(filter_params=filter_params)


class LoadUserId(APIView):
    def get(self, request):
        try:
            username = request.query_params['username']
        except KeyError:
            return invalid_response

        return user.get_user_id(username=username)


class LoadUserGroups(APIView):
    def get(self, request):
        try:
            user_id = request.query_params['userId']
        except KeyError:
            return invalid_response

        return groups.get_users_groups(user_id=user_id)


class UpdateAvatar(APIView):
    def put(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
            url = request.query_params['url']
        except KeyError:
            return invalid_response
        return user.update_avatar(user_id, url)


# ------------------- GROUPS ------------------- #
class Group(APIView):
    # Load group
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
        except KeyError:
            return invalid_response

        return groups.load_group(group_id=group_id)

    # Create Group
    def post(self, request, *args, **kwargs):
        try:
            # This is an example of token checking
#             if not authentic_token(request):
#                 return invalid_token
            title = request.query_params["title"]
            description = request.query_params["description"]
            private = bool(request.query_params["private"])
            user_id = request.query_params["userId"]
        except KeyError:
            content = {
                "reason": "Invalid Request"
            }
            return Response(status=400, data=content)

        group = {
            'title': title,
            'desc': description,
            'private': private
        }

        return groups.create_group(group, user_id=user_id)

    # Delete Group
    def delete(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
        except KeyError:
            return invalid_response

        return groups.delete_group(group_id=group_id)

    # Edit Group
    def put(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
            title = request.query_params["title"]
            description = request.query_params["description"]
            private = bool(request.query_params["private"])
        except KeyError:
            return invalid_response

        group = {
            'id': group_id,
            'title': title,
            'desc': description,
            'private': private
        }

        return groups.edit_group(group)


class LeaveGroup(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.leave_group(user_id=user_id, group_id=group_id)


class JoinGroup(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.join_group(group_id=group_id, user_id=user_id)


class SearchGroups(APIView):
    def get(self, request, *args, **kwargs):
        try:
            search_term = request.query_params["search"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.search_groups(search_term, user_id)


class LoadGroupPosts(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.load_group_posts(group_id, user_id)


class LoadGroupMembers(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
        except KeyError:
            return invalid_response

        return groups.load_group_members(group_id)


class PromoteMember(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
            promote_id = request.query_params["promoteId"]
        except KeyError:
            return invalid_response

        return groups.promote_member(group_id, user_id, promote_id)


class DemoteMember(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
            demote_id = request.query_params["demoteId"]
        except KeyError:
            return invalid_response

        return groups.demote_member(group_id, user_id, demote_id)


class LoadJoinRequest(APIView):
    def get(self, request):
        try:
            group_id = request.query_params["groupId"]
        except KeyError:
            return invalid_response

        return groups.load_join_request(group_id)


class RequestJoinGroup(APIView):
    def get(self, request):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.request_group_invite(group_id=group_id, user_id=user_id)


class AcceptJoinRequest(APIView):
    def get(self, request):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.accept_join_request(group_id=group_id, user_id=user_id)


class DeclineJoinRequest(APIView):
    def get(self, request):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.decline_join_request(group_id=group_id, user_id=user_id)


# ------------------- POSTS ------------------- #

class Post(APIView):
    # Create post
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.query_params["userId"]
            group_id = request.query_params["groupId"]
            post_title = request.query_params["title"]
            post_body = request.query_params["postContent"]
            post_location = request.query_params["location"]
            post_cat = request.query_params["category"]
        except KeyError:
            return invalid_response

        post = {
            'groupId': group_id,
            'author': {
                "userId": user_id,
            },
            'title': post_title,
            'postContent': post_body,
            'location': post_location,
            'category': post_cat
        }

        return posts.create_post(post)

    # Read post
    def get(self, request, *args, **kwargs):
        try:
            post_id = request.query_params["postId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return posts.load_post(post_id=post_id, user_id=user_id)

    # Edit post
    def put(self, request, *args, **kwargs):
        try:
            post_id = request.query_params["postId"]
            user_id = request.query_params["userId"]
            post_title = request.query_params["title"]
            post_content = request.query_params["postContent"]
        except KeyError:
            return invalid_response

        post = {
            "postId": post_id,
            "title": post_title,
            "postContent": post_content
        }
        return posts.edit_post(post=post, user_id=user_id)

    # Delete Post
    def delete(self, request, *args, **kwargs):
        try:
            post_id = request.query_params["postId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return posts.remove_post(post_id=post_id, user_id=user_id)


class LikePost(APIView):
    def get(self, request, *args, **kwargs):
        try:
            post_id = request.query_params["postId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response
        return posts.like_post(post_id=post_id, user_id=user_id)


class UnlikePost(APIView):
    def get(self, request, *args, **kwargs):
        try:
            post_id = request.query_params["postId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response
        return posts.unlike_post(post_id=post_id, user_id=user_id)

# ------------------- COMMENTS ------------------- #

class Comment(APIView):
    # Create
    def post(self, request, *args, **kwargs):
        try:
            post_id = request.query_params['postId']
            user_id = request.query_params['userId']
            content = request.query_params['content']
        except KeyError:
            return invalid_response
        return comments.create_comment(post_id, user_id, content)

    # Read
    def get(self, request, *args, **kwargs):
        try:
            comment_id = request.query_params['commentId']
        except KeyError:
            return invalid_response
        return comments.load_comment(comment_id)

    # Update
    def put(self, request, *args, **kwargs):
        try:
            comment_id = request.query_params['commentId']
            data = None
            if 'content' in request.query_params:
                content = request.query_params['content']
                data = {'content': content}
        except KeyError:
            return invalid_response
        return comments.update_comment(comment_id, data)

    # Delete
    def delete(self, request, *args, **kwargs):
        try:
            comment_id = request.query_params['commentId']
        except KeyError:
            return invalid_response
        return comments.delete_comment(comment_id)


# ------------------- NOTIFICATIONS ------------------- #
class Notification(APIView):
    # Create
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
            group_id = 69
            if 'groupId' in request.query_params:
                group_id = request.query_params['groupId']
            desc = request.query_params['desc']
            note_type = request.query_params['type']
            note = {
                'userId': user_id,
                'groupId': group_id,
                'desc': desc,
                'note_type': note_type
            }
        except KeyError:
            return invalid_response
        return notes.create_notification(note)

    # Read
    def get(self, request, *args, **kwargs):
        try:
            note_id = request.query_params['noteId']
            print("finding note ", note_id)
        except KeyError:
            return invalid_response
        return notes.load_notification(note_id)

    # Update
    def put(self, request, *args, **kwargs):
        try:
            note_id = request.query_params['noteId']
        except KeyError:
            return invalid_response
        return notes.update_notification(note_id)

    # Delete
    def delete(self, request, *args, **kwargs):
        try:
            note_id = request.query_params['noteId']
        except KeyError:
            return invalid_response
        return notes.delete_notification(note_id=note_id)
