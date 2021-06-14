#  -  -  -  -  -  -  #
# CS 314 - Project 3 #
#  -  -  -  -  -  -  #
# user.py
# User management

# Imports
from passlib.handlers.sha2_crypt import sha256_crypt

from .utils.toolbox import gen_response, gen_missing, debug_out
from .utils import response_constants as resp
from .utils.response_constants import RESP_OK, RESP_SERVER, RESP_INVALID, RESP_MISSING
import re
from .models import User, Post, Comment, Group, Member, Note, Friend
from .auth import username_exists, valid_email, valid_password
from . import models
from . import notes

# Relationship Types
# FIXME: We can enum this?
REL_BLOCK = -1
REL_PEND = 0
REL_FRIEND = 1


# Functions

#  -  -  -  -  #
# User admin   #
#  -  -  -  -  #


def get_user_id(username):
    user = models.search_user_by_username(username)

    if user is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif user == -1:
        content = {
            "reason": "User not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    content ={
        "userId": user.user_id
    }
    return gen_response(resp.OK, content)


def load_user(user_id):
    """Gets a user's info from the database

    Parameters
    ----------
    user_id : int
        Unique user identifier

    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation
    """
    #try:
    user = models.search_user(user_id)

    if user is None:
        return gen_response(resp.ERR_MISSING, {"reason": "Failed to find user"})

    user_info = {
        'id': user.user_id,
        'username': user.username,
        'email': user.email,
        'avatar': user.avatar,
        'bio': user.bio
    }

    return gen_response(resp.OK, {"user": user_info})
    #except:
    #    print("load_user failed")
    #    return RESP_SERVER


# FIXME: This still needs queries
def update_user_details(user_info):
    """Updates a user's info in the database

    Parameters
    ----------
    user_info : dict
        JSON representation of user details (updated)

    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation
    """
    try:
        if 'user' in user_info:
            return gen_response(resp.ERR_INVALID, {"reason": "At least provide a user id"})

        user_id = user_info['user_id']
        user = models.search_user(user_id)

        if user is None:
            return gen_missing("user")

        if 'username' in user_info:
            username = user_info['username']
            if not username_exists(username):
                user.username = username
            else:
                return gen_response(resp.ERR_INVALID, {"reason": "Username already exists"})

        if 'email' in user_info:
            email = user_info['email']
            if valid_email(email):
                user.email = email
            else:
                return gen_response(resp.ERR_INVALID, {"reason": "Invalid email"})

        if 'bio' in user_info:
            bio = user_info['bio']
            if len(bio) > 300:
                return gen_response(resp.ERR_INVALID, {"reason": "Bio too long"})
            user.bio = bio

        if 'password' in user_info:
            password = user_info['password']
            if valid_password(password):
                hash_pass = sha256_crypt.encrypt(password)
                user.password = hash_pass
            else:
                return gen_response(resp.ERR_INVALID, {"reason": "Invalid password"})

        models.commit_changes()
        return resp.RESP_OK
    except:
        print("update_user_details failed")
        return RESP_SERVER



def delete_user(user_id):
    """Removes a user from the database
    Parameters
    ----------
    user_id : int
        Unique user identifier
    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation
    """
    try:
        user = models.search_user(user_id)
        if user is None:
            return gen_missing("user")
        # Remove dependencies
        # Comments
        models.remove_user_comments(user_id)
        # Posts
        # TODO: Remove comments on user's posts
        models.remove_user_posts(user_id)
        # Friends
        models.remove_user_relationships(user_id)
        # Members
        models.remove_user_memberships(user_id)
        # Notes
        models.remove_user_notification(user_id)
        # User
        models.remove_user(user_id)
        
        #user.delete()
        #models.commit_changes()
        return resp.RESP_OK
    except:
        return RESP_SERVER


def get_rel_type(id_a, id_b):
    """Gets the type of a relationship between two users

        Parameters
        ----------
        id_a : int
            Username of a person in the relationship

        id_b : int
            Username of another person in the relationship

        Returns
        -------
        dict
            JSON Response detailing the success or failure of operation
        """
    try:
        # TODO: Query
        rel_type = models.get_rel_type(id_a, id_b)

        if rel_type is None:
            return gen_response(resp.ERR_MISSING, {"reason": "Failed to find both users"})

        return gen_response(resp.OK, {"rel_type": rel_type})
    except:
        debug_out("get_rel_type failed")
        return gen_response(resp.ERR_SERVER, {"reason": "Oops! Something went wrong on our end"})


def search_user(search_term, user_id):
    """Search for users based on search term

    Parameters
    ----------
    search_term : str
        Term to search for in usernames
    user_id : str
        Identifier of user who is searching (used to check relationships)
    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation
    """
    try:
        users_found = models.search_users_by_name(search_term)
        print(users_found)
        users = []

        for user in users_found:
            # FIXME:
            #rel = models.get_rel_type(user_id, user.user_id)
            rel = -1;
            #if rel is None:
            #   rel = -1
            users.append({
                'id': user.user_id,
                'username': user.username,
                'avatar': user.avatar,
                'rel': rel,
                'bio': user.bio
            })

        return gen_response(resp.OK, {'content': users})
    except:
        print("search_user incomplete")
        return resp.RESP_SERVER


def add_friend(id_a, id_b):
    """Stores friendship between two users in database

        Parameters
        ----------
        id_a : int
            User id of person adding another

        id_b : int
            User id of person being added

        Returns
        -------
        dict
            JSON Response detailing the success or failure of operation
        """
    try:
        if id_a == id_b:
            return gen_response(resp.ERR_INVALID, {"reason": "If you don't love yourself, how in the hell are you going to add yourself as a friend?"})

        # TODO: Create query
        rel_type = models.get_rel_type(id_a, id_b)

        if rel_type is not None:
            if rel_type == REL_FRIEND:
                return gen_response(resp.ERR_INVALID, {"reason": "Users are already friends"})
            elif rel_type == REL_BLOCK:
                return gen_response(resp.ERR_INVALID, {"reason": "Relationships are blocked between users"})
        # TODO: Create query
        models.set_rel_type(id_a, id_b, REL_FRIEND)
        return gen_response(resp.OK, None)
    except:
        print("add_friend failed")
        return gen_response(resp.ERR_SERVER, {"reason": "Oh no! Our internal issues are getting in the way of companionship D:"})


def invite_friend(id_a, id_b):
    """Person a invites person b as a friend

        Parameters
        ----------
        id_a : int
            User id of person inviting another

        id_b : int
            User id of person being invited

        Returns
        -------
        dict
            JSON Response detailing the success or failure of operation
        """
    try:
        if id_a == id_b:
            return gen_response(resp.ERR_INVALID, {"reason": "If you don't love yourself, how in the hell are you going to add yourself as a friend?"})

        # TODO: Create query
        rel_type = models.get_rel_type(id_a, id_b)

        if rel_type is None:
            # TODO: Create query - set relationship to pending
            models.invite_friend(id_a, id_b)

            try:
                notes.create_friend_request_note(id_a, id_b);
            except:
                print("Failed to create notification: ", id_a, " invited ", id_b)
            return gen_response(resp.OK, None)
        else:
            return gen_response(resp.ERR_INVALID, {"reason": "Cannot invite this user"})
    except:
        print("invite_friend incomplete")
        return gen_response(resp.ERR_SERVER, {"reason": "Oops! Something went wrong D:"})


def update_avatar(user_id, url):

    status = models.update_user_avatar(user_id=user_id, avatar=url)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)
