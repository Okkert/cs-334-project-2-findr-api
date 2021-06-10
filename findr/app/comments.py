#  -  -  -  -  -  -  #
# CS 314 - Project 3 #
#  -  -  -  -  -  -  #
# comments.py
# Comment management

from . import models
from .utils.toolbox import gen_response, gen_missing
from .utils import response_constants as resp
from . import serializers as cereal


# Create
# TODO: Check if user is in group?
def create_comment(post_id, user_id, content):
    """Creates a new comment

    Parameters
    ----------
    post_id : int
        Unique post identifier

    user_id : int
        Unique user identifier

    content : str
        Comment content

    Returns
    -------
    dict
        Response detailing the success or failure of operation
    """
    try:
        if not models.post_exists(post_id):
            return gen_missing("post")
        if not models.user_exists(user_id):
            return gen_missing("user")
        if len(content) > 350:
            return gen_response(status=resp.ERR_INVALID, data={"Comment is too long"})
        models.insert_comment(post_id=post_id, user_id=user_id, comment_content=content)
        return resp.RESP_OK
    except:
        return resp.RESP_SERVER


# Read
# TODO: Check if user is in group
def load_comment(comment_id):
    """Loads an existing comment

    Parameters
    ----------
    comment_id : int
        Unique comment identifier

    Returns
    -------
    dict
        Response detailing the success or failure of operation
    """
    #try:
    comment = models.load_comment(comment_id)
    if comment is None:
        return gen_missing("comment")
    # TODO: Return author (username and avatar) too
    comment_dict = {
        'comment_id': comment.comment_id,
        'post_id': comment.post_id,
        'user_id': comment.user_id,
        'comment_content': comment.comment_content
    }
    return gen_response(status=resp.OK, data=comment_dict)
    #except:
    #    return resp.RESP_SERVER


# Update
# TODO: Check if user is author
def update_comment(comment_id, data=None):
    """Updates an existing comment

    Parameters
    ----------
    comment_id : int
        Unique comment identifier
    data : dict
        Dictionary of comment data to update

    Returns
    -------
    dict
        Response detailing the success or failure of operation
    """
    try:
        if 'content' in data:
            content = data['content']
            if len(content) > 350:
                gen_response(resp.ERR_INVALID, {"reason": "Comments must be 350 characters or less"})
            if not models.update_comment(comment_id, content):
                gen_response(resp.ERR_INVALID, {"reason": "Failed to update comment"})
    except:
        return resp.RESP_SERVER
    return resp.RESP_OK


# Delete
# TODO: Check if user is group admin or author
def delete_comment(comment_id):
    """Removes an existing comment

    Parameters
    ----------
    comment_id : int
        Unique comment identifier

    Returns
    -------
    dict
        Response detailing the success or failure of operation
    """
    #try:
    comment = models.load_comment(comment_id)
    if comment is None:
        return gen_missing("comment")
    models.delete_comment(comment_id)
    return resp.RESP_OK
    #except:
    #    return resp.RESP_SERVER
