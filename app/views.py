from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from . import groups, posts, comments, auth, user, notes
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
            user_id = request.query_params['UserId']
        except KeyError:
            return invalid_response
        return user.delete_user(user_id)


# ------------------- GROUPS ------------------- #
class CreateGroup(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # This is an example of token checking
            if not authentic_token(request):
                return invalid_token
            title = request.query_params["title"]
            description = request.query_params["description"]
            private = bool(request.query_params["private"])
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

        return groups.create_group(group)


class EditGroup(APIView):
    def get(self, request, *args, **kwargs):
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


class DeleteGroup(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
        except KeyError:
            return invalid_response

        return groups.delete_group(group_id=group_id)


class JoinGroup(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
            user_id = request.query_params["userId"]
        except KeyError:
            return invalid_response

        return groups.join_group(group_id=group_id, user_id=user_id)


class LoadGroup(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
        except KeyError:
            return invalid_response

        return groups.load_group(group_id=group_id)


class SearchGroups(APIView):
    def get(self, request, *args, **kwargs):
        try:
            search_term = request.query_params["title"]
        except KeyError:
            return invalid_response

        return groups.search_groups(search_term)


class LoadGroupPosts(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.query_params["groupId"]
        except KeyError:
            return invalid_response

        return groups.load_group_posts(group_id)


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


# ------------------- POSTS ------------------- #
class CreatePost(APIView):
    def get(self, request, *args, **kwargs):
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


# ------------------- COMMENTS ------------------- #
class Notification(APIView):
    # Create
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
            status = request.query_params['status']
            desc = request.query_params['desc']
            note = {
                'user_id': user_id,
                'status': status,
                'desc': desc
            }
        except KeyError:
            return invalid_response
        return notes.create_notification(note)

    # Read
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.query_params['userId']
        except KeyError:
            return invalid_response
        return notes.load_notifications(user_id)

    # Update
    def put(self, request, *args, **kwargs):
        try:
            note_id = request.query_params['noteId']
            data = {
                'note_id': note_id
            }
            if 'status' in request.query_params:
                data['status'] = request.query_params['status']
            if 'desc' in request.query_params:
                data['desc'] = request.query_params['desc']
        except KeyError:
            return invalid_response
        return notes.update_notification(note=data)