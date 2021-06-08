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

# Relationship Types
# FIXME: We can enum this?
REL_BLOCK = -1
REL_PEND = 0
REL_FRIEND = 1


# Functions

#  -  -  -  -  #
# User admin   #
#  -  -  -  -  #


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
    try:
        user = models.search_user(user_id)

        if user is None:
            return gen_response(resp.ERR_MISSING, {"reason": "Failed to find user"})

        user_info = {
            'id': user.user_id,
            'username': user.username,
            'email': user.email,
            # TODO:
            # 'avatar': user.avatar,
            'bio': user.bio
        }

        return gen_response(resp.OK, {"user": user_info})
    except:
        print("load_user failed")
        return RESP_SERVER


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
                user.password = password
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
        user.delete()
        models.commit_changes()
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
        rel_type = models.get_relationship(id_a, id_b)

        if rel_type is None:
            return gen_response(resp.ERR_MISSING, {"reason": "Failed to find both users"})

        return gen_response(resp.OK, {"rel_type": rel_type})
    except:
        debug_out("get_rel_type failed")
        return gen_response(resp.ERR_SERVER, {"reason": "Oops! Something went wrong on our end"})


def search_user(search_term):
    """Search for users based on search term

    Parameters
    ----------
    search_term : str
        Term to search for in usernames

    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation
    """

    # We have to decide whether we want to search similar usernames or usernames that start with the search term
    # OR just users with the exact search term as their username

    # TODO: Search database

    # Query database with chosen search method (exact match / close match)
    # Retrieve usernames from query result and add to list

    # TODO: Retrieve relationship status

    # For each user found, retrieve the relationship status of the found user to the current
    # Relationship status options: You, Friend, Pending, None

    # TODO: Prepare output

    # Collect each search result user's username and relationship status into a dictionary

    # TODO: Return dictionary

    print("search_user incomplete")
    return None


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
            models.set_rel_type(id_a, id_b, rel_type)
            # TODO: Generate notification
            return gen_response(resp.OK, None)
        else:
            return gen_response(resp.ERR_INVALID, {"reason": "Cannot invite this user"})
    except:
        print("invite_friend incomplete")
        return gen_response(resp.ERR_SERVER, {"reason": "Oops! Something went wrong D:"})


def load_feed(user_id):
    """Load's a user's main feed

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

