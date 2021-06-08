from . import models
from .utils.toolbox import gen_response, debug_out, tattle, behaved
from .utils import response_constants as resp


# Function Status: Incomplete but basic implementation, test function created
def create_group(group):
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

    if unique:
        content = {
            "reason": "Group name already exists"
        }
        return gen_response(resp.ERR_INVALID, content)

    status = models.create_group(group_name=group_name, private=private, group_desc=description)

    # TODO Add group creator as a group member and assign them admin roles

    if not status:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Incomplete implementation, basic version working and tested
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
    # TODO: Delete group members and delete group posts
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
    if g is False:
        content = {
            "reason": "Group not found"
        }
        return gen_response(resp.ERR_MISSING, content)

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

    status = models.join_group(group_id=group_id, user_id=user.user_id)

    if not status:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Basic implementation and tests written
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

    # TODO: If user is the only admin then leave request will be denied

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

    status = models.leave_group(group_id=group_id, user_id=user.user_id)

    if status is False:
        content = {
            "reason": "Internal server error"
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
def search_groups(search_term):
    """Search for all groups with a title containing
    the search term

    Parameters
    ----------
    search_term : str
        Name of group that the user would like to leave

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
            groups.append({
                "id": group.group_id,
                "title": group.group_name,
                "desc": group.group_desc
            })

    if groups_desc is not None:
        for group in groups_desc:
            groups.append({
                "id": group.group_id,
                "title": group.group_name,
                "desc": group.group_desc
            })

    response = {
        "status": 200,
        "content": groups
    }

    return gen_response(status=200, data=groups)


# Function Status: Not implemented, need db models to be updated
def load_group_posts(group_id):
    """Loads all posts sent by group members

    Parameters
    ----------
    group_id : int
        ID of group to load posts from

    Returns
    -------
    dict
        JSON Response of all posts made within the group

    """

    content = {
        "reason": "Not implemented yet"
    }
    return gen_response(status=resp.OK, data=content)


# Function Status: Implemented and tested
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
    members = models.load_group_members(group_id=group_id)
    group_members = []
    if members is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    for member in members:
        group_members.append({"user_id": member.user_id})

    response = {
        "status": 200,
        "content": []
    }
    return gen_response(status=resp.OK)


# Function Status: Not implemented, db models need to be updated to indicate admin status
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

    # check if username themselves is an admin, if not return error
    # check if promote_username isn't already an admin
    # update member status of promote_username to admin

    content = {
        "reason": "Not implemented yet"
    }
    return gen_response(resp.OK, content)


# Function Status: Not implemented, db models need to be updated to indicate admin status
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
    # check if username themselves is an admin, if not return error
    # check if demote_username is in fact an admin
    # update member status of demote_username

    content = {
        "reason": "Not implemented yet"
    }
    return gen_response(resp.OK, content)


# Function Status: Not implemented - might be better suited to go in notes.py
def load_join_request():
    """Loads all requests to join the group"""


# Function Status: Not implemented - might be better suited to go in notes.py
def request_group_invite():
    """Sends a request to join the group"""


# Function Status: Not implemented - might be better suited to go in notes.py
def accept_join_request():
    """Accept pending request to join the group"""


# Function Status: Not implemented - might be better suited to go in notes.py
def decline_join_request():
    """Decline pending request to join group"""




