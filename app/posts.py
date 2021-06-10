import requests
import math
from . import models
from .utils.toolbox import gen_response
from .utils import response_constants as resp


API_KEY = "AIzaSyC8GoiY01oowA5Z9rCJGeC2XU40H14Zc2s"


# Function Status: Complete and tested
# TODO: Add category
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
        try:
            post_cat = models.catEnum(post["category"])
        except ValueError:
            content = {
                "reason": "Invalid category selected"
            }
            return gen_response(resp.ERR_INVALID, content)
    except KeyError:
        content = {
            "reason": "Invalid Request"
        }
        return gen_response(resp.ERR_INVALID, content)

    status = models.create_post(user_id, group_id, post_title, post_body, post_location, post_cat)

    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return gen_response(resp.ERR_SERVER, content)

    content = {
        "reason": "Success"
    }
    return gen_response(resp.OK, content)


# Function Status: Complete implementation, but not tested
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

    # If the user attempting to remove the post did not author the post then check if they are an admin
    if user_id != post.user_id:
        member = models.get_group_member(user_id=user_id, group_id=post.group_id)
        if member is False:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)

        if member is not None:
            if member.admin is False:
                content = {
                    "reason": "User does not have permissions to delete this post"
                }
                return gen_response(resp.ERR_UNAUTH, content)
        else:
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


# Function Status: Complete and tested
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


# Function Status: Basic implementation, tested
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

    user = models.search_user_by_id(user_id=post.user_id)

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
        "groupId": 11,  # FIXME: Need to add group_id column to db
        "postId": post_id,
        "author": {
            "userId": post.user_id,
            "username": user.username,
            "avatar": "path/to/avatar"  # TODO: Add path to avatar
        },
        "title": post.post_title,
        "postContent": post.post_desc,
        "likes": post.post_likes,
        "hasLiked": has_liked,
        "postLocation": post.post_loc,
        "postTime": post.post_time,
        "postCategory": str(repr(models.catEnum(post.post_cat))).split("'")[1],
        "postComments": post_comments
    }
    return gen_response(resp.OK, content)


def load_feed(filter):
    """
        filter: dict
            userId : int
            type : str
            location : str, optional
            distance : int, optional
            username : int, optional
            groupId : int, optional
            category : str, optional

    """

    try:
        filter_type = filter["type"]
        user_id = filter["userId"]
    except KeyError:
        content = {
            "reason": "Invalid request"
        }
        return gen_response(resp.ERR_INVALID, content)

    # --------------------- PREAMBLE --------------------- #
    user_feed = []
    if filter_type == "Time" or filter_type == "Location" or filter_type == "Category" or filter_type == "User":
        user_groups = models.get_users_groups(user_id=user_id)
        if user_groups is None:
            content = {
                "reason": "User is not in any groups",
                "posts": []
            }
            return gen_response(resp.OK, content)
        elif user_groups is False:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)
        if filter_type != "Category" or filter_type != "User":
            for group in user_groups:
                posts = load_group_posts(group.group_id)
                try:
                    user_feed += posts["posts"]
                except KeyError:
                    content = {
                        "reason": posts["reason"]
                    }
                    return gen_response(posts["code"], content)

    # --------------------- TIME --------------------- #
    # Sorts all posts by most recent
    if filter_type == "Time":
        post_data = sorted(user_feed, key=lambda i: i['postTime'])

        content = {
            "posts": post_data
        }

        return gen_response(resp.OK, content)

    # --------------------- LOCATION --------------------- #
    # Returns posts within the specified distance of input location
    if filter_type == "Location":
        try:
            location = filter["location"]
            try:
                distance = float(filter["distance"])
            except KeyError:
                distance = 10.0
        except KeyError:
            content = {
                "reason": "Invalid request"
            }
            return gen_response(resp.ERR_INVALID, content)

        base_location = get_lat_long(location=location)
        if base_location is False:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)

        post_data = []
        for post in user_feed:
            target_location = get_lat_long(post["postLocation"])
            dist_to_base = calculate_distance(base_lat=base_location[0], base_long=base_location[1],
                                              target_lat=target_location[0], target_long=target_location[1])

            if dist_to_base <= distance:
                post_data.append(post)

        content = {
            "posts": post_data
        }
        return gen_response(resp.OK, content)


    # --------------------- CATEGORY --------------------- #
    # Get all posts from that category and check if the user is in the group of the category
    if filter_type == "Category":
        try:
            try:
                category = models.catEnum(filter["category"])
            except ValueError:
                content = {
                    "reason": "Invalid category selected"
                }
                return gen_response(resp.ERR_INVALID, content)
        except KeyError:
            content = {
                "reason": "Invalid request"
            }
            return gen_response(resp.ERR_INVALID, content)

        post_data = []
        for group in user_groups:
            posts = get_category_posts(category=category, group_id=group.group_id)
            if posts is False:
                content = {
                    "reason": "Internal server error"
                }
                return gen_response(resp.ERR_SERVER, content)
            post_data += posts

        content = {
            "posts": post_data
        }
        return gen_response(resp.OK, content)


    # --------------------- USER --------------------- #
    # Returns all post made by the input user within the searching users groups
    if filter_type == "User":
        try:
            username = filter["username"]
        except KeyError:
            content = {
                "reason": "Invalid Request"
            }
            return gen_response(resp.ERR_INVALID, content)

        user = models.search_user_by_username(username=username)

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

        post_data = []
        for group in user_groups:
            posts = get_user_posts(user, group.group_id)
            if posts is False:
                content = {
                    "reason": "Internal server error"
                }
                return gen_response(resp.ERR_SERVER, content)
            post_data += posts

        content = {
            "posts": post_data
        }
        return gen_response(resp.OK, content)

    # --------------------- GROUP --------------------- #
    if filter_type == "Group":
        try:
            group_id = filter["groupId"]
        except KeyError:
            content = {
                "reason": "Invalid Request"
            }
            return gen_response(resp.ERR_INVALID, content)

        posts = load_group_posts(group_id=group_id)
        try:
            post_data = posts["posts"]
        except KeyError:
            content = {
                "reason": posts["reason"]
            }
            return gen_response(posts["code"], content)

        content = {
            "posts": post_data
        }
        return gen_response(resp.OK, content)

# ------------------
# Helper Functions
# ------------------


def calculate_distance(base_lat, base_long, target_lat, target_long):
    earth_radius = 6373.0

    base_lat = math.radians(base_lat)
    base_long = math.radians(base_long)

    target_lat = math.radians(target_lat)
    target_long = math.radians(target_long)

    long_distance = target_long - base_long
    lat_distance = target_lat - base_lat

    # Haversine formula
    a = math.sin(lat_distance / 2) ** 2 + math.cos(base_lat) * math.cos(target_lat) * math.sin(long_distance / 2) ** 2
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * b

    return distance


def get_lat_long(location):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"
    response = requests.get(url=url)
    data = response.json()
    if data["status"] == "OK":
        lat = float(data["results"][0]["geometry"]["location"]["lat"])
        long = float(data["results"][0]["geometry"]["location"]["lng"])
        return [lat, long]
    else:
        return False


def get_category_posts(category, group_id):
    posts = models.get_posts_from_category(category=category, group_id=group_id)
    if posts is False:
        return False

    post_data = format_posts(posts)
    return post_data


def get_user_posts(user, group_id):
    posts = models.get_posts_from_user(user_id=user.user_id, group_id=group_id)

    if posts is False:
        return False

    post_data = format_posts(posts)
    return post_data


def format_posts(posts):
    post_data = []
    for post in posts:

        user = models.search_user_by_id(user_id=post.user_id)

        if user is False:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)
        elif user == -1:
            content = {
                "reason": "Post author not found"
            }
            return gen_response(resp.ERR_MISSING, content)

        comment_data = []

        comments = models.get_comments(post_id=post.post_id)

        for comment in comments:
            author = models.search_user_by_id(user_id=comment.user_id)
            comment_data.append({
                "author": {
                    "userId": author.user_id,
                    "username": author.username,
                    "avatar": "/path/to/avatar"  # TODO
                },
                "commentContent": comment.comment_content,
                "commentTime": comment.comment_time,

            })

        post_data.append({
            "postId": post.post_id,
            "groupId": post.group_id,
            "author": {
                "userId": post.user_id,
                "username": user.username,
                "avatar": "/path/to/avatar"  # TODO
            },
            "title": post.post_title,
            "postCategory": str(repr(models.catEnum(post.post_cat))).split("'")[1],
            "likes": post.post_likes,
            "postComments": comment_data,
            "postTime": post.post_time,
            "postLocation": post.post_loc
        })

    return post_data


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
    group = models.search_group_by_id(group_id=group_id)
    if group is None:
        content = {
            "reason": "Group not found",
            "code": resp.ERR_MISSING
        }
        return content

    posts = models.load_group_posts(group_id=group_id)
    if posts is False:
        content = {
            "reason": "Internal server error",
            "code": resp.ERR_SERVER

        }
        return content

    post_data = []
    for post in posts:
        comment_data = []
        user = models.search_user_by_id(user_id=post.user_id)
        comments = models.get_comments(post_id=post.post_id)
        if len(comments) != 0:
            for comment in comments:
                author = models.search_user_by_id(user_id=comment.user_id)
                comment_data.append({
                    "author": {
                        "userId": author.user_id,
                        "username": author.username,
                        "avatar": "/path/to/avatar"  # TODO
                    },
                    "commentContent": comment.comment_content,
                    "commentTime": comment.comment_time,

                })

        if user is False:
            content = {
                "reason": "Internal server error",
                "code": resp.ERR_SERVER
            }
            return content

        elif user == -1:
            content = {
                "reason": "User not found",
                "code": resp.ERR_MISSING
            }
            return content

        post_data.append({
            "postId": post.post_id,
            "groupId": post.group_id,
            "author": {
                "userId": post.user_id,
                "username": user.username,
                "avatar": "/path/to/avatar"  # TODO
            },
            "title": post.post_title,
            "postCategory": str(repr(models.catEnum(post.post_cat))).split("'")[1],
            "likes": post.post_likes,
            "postComments": comment_data,
            "postTime": post.post_time,
            "postLocation": post.post_loc
        })
    content = {
        "posts": post_data
    }
    return content
