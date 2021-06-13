from . import models
from .utils.toolbox import gen_response, debug_out, tattle, behaved
from .utils import response_constants as resp


# Function Status: Complete and tested
def create_group(group, user_id):
    """ Creates a new group

    Parameters
    ----------
    group : dict
        title: str:
            Group name

        description : str
            The description of the group

        private : bool
            True if the group is private, False otherwise

    user_id : int
        ID of the user creating the group

    Returns
    -------
    dict
        JSON Response detailing the success or failure of group creation

    """
    try:
        group_name = group["title"]
        private = group["private"]
        description = group["desc"]
    except KeyError:
        content = {
            "reason": "Invalid Request"
        }
        return gen_response(resp.ERR_INVALID, content)

    unique = models.search_group_by_name(group_name=group_name)

    if unique is not None:
        content = {
            "reason": "Group name already exists"
        }
        return gen_response(resp.ERR_INVALID, content)

    status = models.create_group(group_name=group_name, private=private, group_desc=description)

    if not status:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    # Add group creator as a group member and assign them admin roles
    g = models.search_group_by_name(group_name=group_name)
    if g is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    status = models.join_group(group_id=g.group_id, user_id=user_id, membership=2)

    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def delete_group(group_id):
    """Deletes a group from the database, update
    membership statuses and lose posts.

    Parameters
    ----------
    group_id : str
        ID of group to delete

    Returns
    -------
    dict
        JSON Response detailing the success or failure of group deletion

    """

    # Delete all posts associated with group
    status = models.delete_group_posts(group_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    # Delete all members associated with group
    status = models.delete_group_members(group_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    status = models.delete_group(group_id)

    if status == -1:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def edit_group(group):
    """Edits group info

    Parameters
    ----------
    group : dict
        Group object

        id : int
            Group ID

        title : str
            Updated group description

        private : int
            Updated group privacy status

        desc : str
            Updated group description

    Returns
    -------
    dict
        JSON Response detailing the success or failure of group detail update

    """
    try:
        group_id = group["id"]
        updated_group_title = group["title"]
        updated_group_desc = group["desc"]
        updated_private = group["private"]
    except KeyError:
        content = {
            "reason": "Invalid Request"
        }
        return gen_response(resp.ERR_INVALID, content)

    g = models.search_group_by_id(group_id)
    if g is None:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    elif g is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    if g.private != updated_private:
        status = models.update_group_private(group_id=group_id, updated_private=updated_private)
        if not status:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)

    if g.group_name != updated_group_title:
        status = models.update_group_name(group_id=group_id, updated_name=updated_group_title)
        if not status:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)

    if g.group_desc != updated_group_desc:
        status = models.update_group_desc(group_id=group_id, updated_desc=updated_group_desc)
        if not status:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
# TODO: If group is private then send join request or error message maybe
def join_group(user_id, group_id):
    """Adds a user to a group

    Parameters
    ----------
    group_id : int
        ID of group that the user would like to join

    user_id : int
        ID of user that would like to join the group

    Returns
    -------
    dict
        JSON Response detailing the success or failure of group join request

    """
    user = models.search_user_by_id(user_id)
    if user == -1:
        content = {
            "reason": "User not found"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif user is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    group = models.search_group_by_id(group_id=group_id)
    if group is None:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif group is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    status = models.join_group(group_id=group_id, user_id=user.user_id, membership=1)

    if not status:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete, not tested
def leave_group(user_id, group_id):
    """Removes user from a group

    Parameters
    ----------
    group_id : int
        ID of group that the user would like to leave

    user_id : int
        ID of user that would like to leave the group

    Returns
    -------
    dict
        JSON Response detailing the success or failure of leave request

    """

    # If user is the only admin then leave request will be denied
    admins = models.get_group_admins(group_id=group_id)
    member = models.get_group_member(user_id=user_id, group_id=group_id)
    if admins is False or member is False:
        content = {
            "reason": "Internal server error encountered when trying to get user membership status"
        }
        return gen_response(resp.ERR_SERVER, content)

    if member is None:
        content = {
            "reason": "User is not a member of the group"
        }
        return gen_response(resp.ERR_MISSING, content)

    if len(admins) == 1 and member.membership == 2:
        content = {
            "reason": "User is the only admin, please promote another admin before attempting to leave"
        }
        return gen_response(resp.ERR_INVALID, content)

    user = models.search_user_by_id(user_id)
    if user == -1:
        content = {
            "reason": "User not found"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif user is False:
        content = {
            "reason": "Internal server error encountered when trying to locate user"
        }
        return gen_response(resp.ERR_SERVER, content)

    status = models.leave_group(group_id=group_id, user_id=user.user_id)

    if status is False:
        content = {
            "reason": "Internal server error encountered when trying to leave group"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif status == -1:
        content = {
            "reason": "User is not a member of the group"
        }
        return gen_response(resp.ERR_MISSING, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def load_group(group_id=None, group_name=None):
    """Loads all group info, at least 1 parameter should be given

    Parameters
    ----------
    group_id : int, optional
        Group id of the group to load

    group_name : str optional
        Group name of the group to load

    Returns
    -------
    dict
        JSON Response detailing the success or failure of leave request

    """
    if group_id is None and group_name is None:
        content = {
            "reason": "Invalid request"
        }
        return gen_response(resp.ERR_INVALID, content)

    if group_id is not None:
        g = models.search_group_by_id(group_id)
    else:
        g = models.search_group_by_name(group_name)

    if not g:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    content = {
        "id": g.group_id,
        "title": g.group_name,
        "private": g.private,
        "desc": g.group_desc
    }

    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def search_groups(search_term, user_id):
    """Search for all groups with a title containing
    the search term

    Parameters
    ----------
    search_term : str
        Name of group that the user would like to leave

    user_id : int
        ID of the user making the search

    Returns
    -------
    dict
        JSON Response of all groups found as well as whether the user is
        a member of the group

    """
    groups = []
    groups_name = models.search_groups_by_name(search_term)
    groups_desc = models.search_groups_by_desc(search_term)

    if groups_name is False or groups_desc is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    if groups_name is not None:
        for group in groups_name:
            membership = models.get_group_member(user_id, group.group_id)
            if membership is False:
                content = {
                    "reason": "Internal server error"
                }
                return gen_response(resp.ERR_SERVER, content)

            if membership is None:
                mem = -1
            else:
                mem = membership.membership

            groups.append({
                "id": group.group_id,
                "title": group.group_name,
                "desc": group.group_desc,
                "membership": mem,
                "private": group.private
            })

    if groups_desc is not None:
        for group in groups_desc:
            membership = models.get_group_member(user_id, group.group_id)
            if membership is False:
                content = {
                    "reason": "Internal server error"
                }
                return gen_response(resp.ERR_SERVER, content)

            if membership is None:
                mem = -1
            else:
                mem = membership.membership

            groups.append({
                "id": group.group_id,
                "title": group.group_name,
                "desc": group.group_desc,
                "membership": mem,
                "private": group.private
            })

    content = {
        "groups": groups
    }

    return gen_response(status=200, data=content)


# Function Status: Complete and tested
def load_group_posts(group_id, user_id):
    """Loads all posts sent by group members

    Parameters
    ----------
    group_id : int
        ID of group to load posts from

    user_id : int
        ID of the user

    Returns
    -------
    dict
        JSON Response of all posts made within the group

    """
    group = models.search_group_by_id(group_id=group_id)
    if group is None:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    posts = models.load_group_posts(group_id=group_id)
    if posts is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    post_data = []
    for post in posts:
        comment_data = []
        user = models.search_user_by_id(user_id=post.user_id)
        comments = models.get_comments(post_id=post.post_id)

        for comment in comments:
            author = models.search_user_by_id(user_id=comment.user_id)
            comment_data.append({
                "author": {
                    "userId": author.user_id,
                    "username": author.username,
                    "avatar": author.avatar
                },
                "commentContent": comment.comment_content,
                "commentTime": comment.comment_time,

            })

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

        has_liked = models.has_liked(user_id=user_id, post_id=post.post_id)

        if has_liked == -1:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)

        post_data.append({
            "postId": post.post_id,
            "groupId": post.group_id,
            "author": {
                "userId": post.user_id,
                "username": user.username,
                "avatar": user.avatar
            },
            "title": post.post_title,
            "postCategory": str(repr(models.catEnum(post.post_cat))).split("'")[1],
            "likes": post.post_likes,
            "hasLiked": has_liked,
            "postComments": comment_data,
            "postContent": post.post_desc,
            "postTime": post.post_time,
            "postLocation": post.post_loc,
        })
    content = {
        "posts": post_data
    }
    return gen_response(status=resp.OK, data=content)


# Function Status: Complete and tested
def load_group_members(group_id):
    """Loads all group members

    Parameters
    ----------
    group_id : int
        ID of group to load members from

    Returns
    -------
    dict
        JSON Response of all members within the group

    """
    group = models.search_group_by_id(group_id=group_id)
    if group is None:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    members = models.load_group_members(group_id=group_id)
    group_members = []
    if members is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    for member in members:
        group_members.append({"userId": member.user_id, "membershipStatus": member.membership})

    content = {
        "members": group_members
    }
    return gen_response(status=resp.OK, data=content)


# Function Status: Complete and tested
def promote_member(group_id, user_id, promote_user_id):
    """Grants admin permissions to a group member

    Parameters
    ----------
    group_id: int
        Name of group to load members from

    user_id : int
        Username of person granting admin permissions

    promote_user_id: int
        Username of the person to grant admin permissions to

    Returns
    -------
    dict
        JSON Response detailing the success or failure of member promotion

    """
    user = models.get_group_member(user_id=user_id, group_id=group_id)
    promote_user = models.get_group_member(user_id=promote_user_id, group_id=group_id)

    if user is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif user is None:
        content = {
            "reason": "User is not a member of the group"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif user.membership != 2:
        content = {
            "reason": "User is not permitted to promote members to admin"
        }
        return gen_response(resp.ERR_INVALID, content)

    if promote_user is None:
        content = {
            "reason": "The user you are tying to promote is not a member of the group or the group may not exist"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif promote_user is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    status = models.promote_user(user_id=promote_user_id, group_id=group_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def demote_member(group_id, user_id, demote_user_id):
    """Removes a member's admin permissions

    Parameters
    ----------
    group_id : int
        Name of group to load members from

    user_id : int
        Username of person granting admin permissions

    demote_user_id: int
        Username of the person to remove admin permissions from

    Returns
    -------
    dict
        JSON Response detailing the success or failure of member demotion

    """
    user = models.get_group_member(user_id=user_id, group_id=group_id)
    demote_user = models.get_group_member(user_id=demote_user_id, group_id=group_id)
    if user is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif user is None:
        content = {
            "reason": "User is not a member of the group or the group may not exist"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif user.membership != 2:
        content = {
            "reason": "User is not permitted to demote members to admin"
        }
        return gen_response(resp.ERR_INVALID, content)

    if demote_user is None:
        content = {
            "reason": "The user you are tying to demote is not a member of the group"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif demote_user is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    status = models.demote_user(user_id=demote_user_id, group_id=group_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def load_join_request(group_id):
    """Loads all requests to join the group"""

    join_requests = models.load_join_request(group_id=group_id)
    if join_requests is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    requests = []
    for request in join_requests:
        user = models.search_user_by_id(user_id=request.user_id)
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

        requests.append({
            "userId": request.user_id,
            "username": user.username,
            "avatar": "path/to/avatar"  # TODO
        })

    content = {
        "requests": requests
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
# TODO: Send notification to admins about join request
def request_group_invite(group_id, user_id):
    """Sends a request to join the group to the admins of the group and sets
    membership status to pending

    Parameters
    ----------
    group_id : int
        ID of group to request invite to

    user_id: int
        ID of the user requesting the invite

    Returns
    -------
    dict
        JSON Response detailing the success or failure of the group invite request

    """
    group = models.search_group_by_id(group_id=group_id)
    if group is None:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    user = models.search_user_by_id(user_id=user_id)
    if user == -1:
        content = {
            "reason": "User not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    # Get admins of group
    admins = models.get_group_admins(group_id)

    # TODO:
    # For each admin create a notification
    if admins is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    if len(admins) == 0:
        content = {
            "reason": "There are no group admins to send the join request to"
        }
        return gen_response(resp.ERR_INVALID, content)

    # for admin in admins:
    #     # Send the admin a notification
    #     user = models.search_user_by_id(user_id=user_id)
    #     if user is False:
    #         content = {
    #             "reason": "Internal server error"
    #         }
    #         return gen_response(resp.ERR_SERVER, content)
    #     elif user == -1:
    #         content = {
    #             "reason": "User not found"
    #         }
    #         return gen_response(resp.ERR_MISSING, content)

    # Check if request has already been made
    member = models.get_group_member(user_id=user_id, group_id=group_id)
    if member is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif member is not None:
        content = {
            "reason": "Request has already been sent"
        }
        return gen_response(resp.OK, content)

    status = models.request_group_invite(group_id=group_id, user_id=user_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }

    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def accept_join_request(group_id, user_id):
    """Accept pending request to join the group

    Parameters
    ----------
    group_id : int
        ID of group to accept the join request to

    user_id: int
        ID of the user to add to the group

    Returns
    -------
    dict
        JSON Response detailing the success or failure of the accept join request

    """

    group = models.search_group_by_id(group_id=group_id)
    if group is None:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    user = models.search_user_by_id(user_id=user_id)
    if user == -1:
        content = {
            "reason": "User not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    status = models.accept_join_request(group_id=group_id, user_id=user_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif status == -1:
        content = {
            "reason": "Member requesting invite either not found or request has been accepted"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete and tested
def decline_join_request(group_id, user_id):
    """Decline pending request to join group

    Parameters
    ----------
    group_id : int
        ID of group to accept the join request to

    user_id: int
        ID of the user to add to the group

    Returns
    -------
    dict
        JSON Response detailing the success or failure of the decline join request

    """

    group = models.search_group_by_id(group_id=group_id)
    if group is None:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    user = models.search_user_by_id(user_id=user_id)
    if user == -1:
        content = {
            "reason": "User not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    status = models.decline_join_request(group_id=group_id, user_id=user_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif status == -1:
        content = {
            "reason": "Member not found"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


def get_users_groups(user_id):

    user_id = int(user_id)
    g = models.get_users_groups(user_id=user_id)

    if g is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    groups = []

    if len(g) != 0:
        for group in g:
            group_id = group.group_id
            membership = group.membership
            group_name = models.search_group_by_id(group_id=group_id)
            if group_name is False:
                content = {
                    "reason": "Internal server error"
                }
                return gen_response(resp.ERR_SERVER, content)

            group_name = group_name.group_name

            groups.append({
                "groupName": group_name,
                "groupId":  group_id,
                "membership": membership
            })

    content = {
        "groups": groups
    }
    return gen_response(resp.OK, content)

