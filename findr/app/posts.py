from . import models
from .utils.toolbox import gen_response
from .utils import response_constants as resp


# Function Status: Basic implementation, not tested
# and Post table needs to be adapted to accept group information
def create_post(post):
    """ Creates a new group and sets the creator as admin

    Parameters
    ----------
    post : dict
        <groupId> : int
        <author> : dict
            <userId> : int
            <username> : str
            <avatar> : str
        <title> : str
        <postContent> : str
        <location> : str
        <category> : enum

    Returns
    -------
    dict
        JSON Response detailing the success or failure of post creation

    """
    try:
        user_id = post["author"]["userId"]
        group_id = post["groupId"]
        post_title = post["title"]
        post_body = post["postContent"]
        post_location = post["location"]
        post_cat = post["category"]
    except KeyError:
        content = {
            "reason": "Invalid Request"
        }
        return gen_response(resp.ERR_INVALID, content)

    status = models.create_post(user_id, group_id, post_title, post_body, post_location, post_cat)

    if not status:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Incomplete implementation, but tested
def remove_post(post_id, user_id):
    """Removes a post from Findr

    Parameters
    ----------
    post_id : int
        ID of the post to remove

    user_id : int
        ID of the user attempting to remove the post

    Returns
    -------
    dict
        JSON Response detailing the success or failure of post removal

    """

    post = models.load_post(post_id)

    if post is None:
        content = {
            "reason": "Post not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    if user_id != post.user_id:
        # TODO:
        # If user does not own the post, check if they are the admin of the group
        # group_id = post.group_id
        # Get admins of group
        # Cross reference against user making delete request
        # Proceed accordingly

        content = {
            "reason": "User does not have permissions to delete this post"
        }
        return gen_response(resp.ERR_UNAUTH, content)

    status = models.remove_comments(post_id=post_id)
    if not status:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    status = models.remove_post(post_id=post_id)
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
def edit_post(post, user_id):
    """Edits group info

    Parameters
    ----------
    post : dict
        <postId> : int
        <groupId> : int
        <author> : dict
            <userId> : int
        <title> : str
        <postContent> : str

    user_id : int
        ID of the user making the edit

    Returns
    -------
    dict
        JSON Response detailing the success or failure of post edit

    """
    try:
        post_id = post["postId"]
        author_id = post["author"]["userId"]
        post_title = post["title"]
        post_content = post["postContent"]
    except KeyError:
        content = {
            "reason": "Invalid Request"
        }
        return gen_response(resp.ERR_INVALID, content)

    if author_id != user_id:
        content = {
            "reason": "User does not have permissions to delete this post"
        }
        return gen_response(resp.ERR_UNAUTH, content)

    status = models.edit_post_title(post_id=post_id, post_title=post_title)
    if not status:
        content = {
            "reason": "Post not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    status = models.edit_post_desc(post_id=post_id, post_desc=post_content)
    if not status:
        content = {
            "reason": "Post not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Incomplete implementation, but tested
def like_post(post_id, user_id):
    """Likes a post

    Parameters
    ----------
    post_id : int
        ID of the post to like

    post_id : int
        ID of the user liking the post

    Returns
    -------
    dict
        JSON Response detailing the success or failure of the like

    """

    # TODO Keep track of if the user has already liked the post

    status = models.like_post(post_id=post_id)
    if status == -1:
        content = {
            "reason": "Post not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete not tested
def post_comment(post_id, comment):
    """Comment on a post

    Parameters
    ----------
    post_id : int
        ID of the post to comment on

    comment: dict
        <authorID> : int
        <commentContent> : str

    Returns
    -------
    dict
        JSON Response detailing the success or failure of the comment post
    """
    try:
        user_id = comment["authorId"]
        comment_content = comment["commentContent"]
    except KeyError:
        content = {
            "reason": "Invalid Request"
        }
        return gen_response(resp.ERR_INVALID, content)

    # TODO: Check if user and post are valid users and posts
    post = models.load_post(post_id=post_id)
    if post is None:
        content = {
            "reason": "Post not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    user = models.search_user_by_id(user_id=user_id)

    if user == -1:
        content = {
            "reason": "User not found"
        }
        return gen_response(resp.ERR_MISSING, content)

    status = models.post_comment(post_id=post_id, user_id=user_id, comment_content=comment_content)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Basic implementation, almost complete, not tested
# TODO: Get path to avatar
# TODO: Return whether the user has liked the post
def load_post(post_id):
    """Loads post information

    Parameters
    ----------
    post_id : int
        ID of post you want to load

    Returns
    -------
    dict
        JSON Response with information about the specified post

    """
    post = models.load_post(post_id=post_id)
    user = models.search_user_by_id(user_id=post.user_id)

    if post is None:
        content = {
            "reason": "Post not found"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif post is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    if user == -1:
        content = {
            "reason": "Post not found"
        }
        return gen_response(resp.ERR_MISSING, content)
    elif user is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    # TODO: Check if the user id is in the liked array if yes has_liked = True

    has_liked = False

    comments = models.get_comments(post_id=post_id)
    post_comments = []
    if comments is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)
    elif comments is not None:
        for comment in comments:
            commenter = models.search_user_by_id(comment.user_id)
            if commenter == -1:
                content = {
                    "reason": "Post not found"
                }
                return gen_response(resp.ERR_MISSING, content)
            elif commenter is False:
                content = {
                    "reason": "Internal server error"
                }
                return gen_response(resp.ERR_SERVER, content)

            post_comments.append({
                "author": {
                    "userId": comment.user_id,
                    "username": commenter.username,
                    "avatar": "path/to/avatar"
                },
                "commentContent": comment.comment_content,
                "commentTime": comment.comment_time,
            })

    content = {
        "groupId": 11, # FIXME: Need to add group_id column to db
        "postId": post_id,
        "author": {
            "userId": post.user_id,
            "username": user.username,
            "avatar": "path/to/avatar" # TODO: Add path to avatar
        },
        "title": post.post_title,
        "postContent": post.post_desc,
        "likes": post.post_likes,
        "hasLiked": has_liked,
        "postLocation": post.post_loc,
        "postTime": post.post_time,
        "category": post.category,
        "postComments": post_comments
    }
    return gen_response(resp.OK, content)
