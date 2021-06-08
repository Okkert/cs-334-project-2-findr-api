from django.test import TestCase
from findr.app.auth import register, login, logout
from findr.app.utils.toolbox import debug_out
import findr.app.posts as posts
import findr.app.groups as groups


# ---------------------------- POSTS TESTS ------------------------------- #
def test_create_post(mode):
    """Tests create_post()

    Parameters
    ----------
    mode : int
        If mode is 1 it tests a legitimate create post, 2 tests a server error
        and 3 tests incorrect input
    """
    post = {}
    if mode == 1:
        post = {
            "groupId": 11,
            "author": {
                "userId": 2,
                "username": "Swingeon\n",
                "avatar": "path/to/jane42.png\n"
            },
            "title": "Happy Birthday to Me",
            "postContent": "Why did no one show up to my Spur birthday",
            "location": "Stellenbosch",
            "category": "Hot tub"
        }
    elif mode == 2:
        post = {
            "groupId": -1,
            "author": {
                "userId": 17,
                "username": "DanieDuikboot\n",
                "avatar": "path/to/jane42.png\n"
            },
            "title": "Happy Birthday to Me",
            "postContent": "Why did no one show up to my Spur birthday",
            "location": "Stellenbosch",
            "category": "Hot tub"
        }
    elif mode == 3:
        post = {
            "author": {
                "userId": 17,
                "username": "DanieDuikboot\n",
                "avatar": "path/to/jane42.png\n"
            },
            "title": "Happy Birthday to Me",
            "postContent": "Why did no one show up to my Spur birthday",
            "location": "Stellenbosch",
        }

    response = posts.create_post(post)
    print(response)


def test_remove_post(mode, post_id):
    if mode == 1:
        response = posts.remove_post(post_id, 2)
    if mode == 2:
        response = posts.remove_post(post_id, -1)
    if mode == 3:
        response = posts.remove_post(-1, 2)

    print(response)


def test_edit_post(mode):
    if mode == 1:
        post = {
            "postId": 14,
            "groupId": 11,
            "author": {
                "userId": 2,
            },
            "title": "Jane betrayed me",
            "postContent": "Jane we're breaking up"
        }
        user_id = 2
        response = posts.edit_post(post, 2)

    if mode == 2:
        post = {
            "postId": 10,
            "groupId": 11,
            "author": {
                "userId": 2,
            },
            "title": "Jane betrayed me",
            "postContent": "Jane we're breaking up"
        }
        user_id = 2
        response = posts.edit_post(post, 2)

    if mode == 3:
        post = {
            "groupId": 11,
            "author": {
                "userId": 2,
            },
            "title": "Jane betrayed me",
            "postContent": "Jane we're breaking up"
        }
        user_id = 2
        response = posts.edit_post(post, 2)

    print(response)


def test_like_post(mode):
    if mode == 1:
        response = posts.like_post(14, 2)
    if mode == 2:
        response = posts.like_post(-1, 2)
    if mode == 3:
        response = posts.like_post(14, -1)


def test_post_comment(mode):
    if mode == 1:
        comment = {
            "authorId": 2,
            "commentContent": "I don't care about hot tubs, only beets, bears and battlestar galactica"
        }
        posts.post_comment(14, comment)
    if mode == 2:
        comment = {
            "authorId": 2,
            "commentContent": "I don't care about hot tubs, only beets, bears and battlestar galactica"
        }
        posts.post_comment(-1, comment)
    if mode == 3:
        comment = {
            "commentContent": "I don't care about hot tubs, only beets, bears and battlestar galactica"
        }
        posts.post_comment(14, comment)



# ---------------------------- GROUP TESTS ------------------------------- #
def test_create_group(mode):
    """Tests create_group()

    Parameters
    ----------
    mode : int
        If mode is 1 it tests a legitimate create group, 2 tests a bad request
    """

    if mode == 1:
        group = {
            "title": "Jane's Hot Tub Party",
            "desc": "I bought a hot tub, who wants to be my twitch mod?\n",
            "private": True
        }

    if mode == 2:
        group = {
            "title": "Jane's Hot Tub Party",
        }

    response = groups.create_group(group)
    print(response)


def test_load_group(mode, group_id):
    """Tests load_group()

    Parameters
    ----------
    mode : int
        If mode is 1 it tests load_group() with a legitimate group_id, if mode
        is 2 it tests with a non-existent group ID and if mode is 3 it tests a bad request
    """
    if mode == 1:
        response = groups.load_group(group_id=group_id)
    if mode == 2:
        response = groups.load_group(group_id=-1)
    if mode == 3:
        response = groups.load_group()

    print(response)


def test_delete_group(mode, group_id):
    """Tests load_group()

    Parameters
    ----------
    mode : int
        If mode is 1 it tests delete_group() by group id, if mode is 2 it tests delete_group()
        with an invalid ID, if mode is 3, it tests a bad request
    """
    if mode == 1:
        response = groups.delete_group(group_id=group_id)
    if mode == 2:
        response = groups.load_group(group_id=-1)
    if mode == 3:
        response = groups.load_group()

    print(response)


def test_edit_group(mode):
    """Tests load_group()

    Parameters
    ----------
    mode : int
        If mode is 1 it tests load_group() by group name, if mode is 2 it tests load_group()
        by id, if mode is 3 it tests with a non-existent group and if mode is 4 it tests a bad request
    """
    if mode == 1:
        # group = {
        #     "title": "Susan's Thruple",
        #     "desc": "Welcome to my thruple\n",
        #     "private": True
        # }
        # response = groups.create_group(group)
        # print(f"Created group with response:\n{response}")
        group = {
            "id": 11,
            "title": "Suzie",
            "desc": "Good boys share their toys and hot tubs\n",
            "private": True
        }
        response = groups.edit_group(group)
    if mode == 2:
        response = groups.load_group(group_id=-1)
    if mode == 3:
        response = groups.load_group(group_id=-1)
    if mode == 4:
        response = groups.load_group()
    print(response)


def test_join_group(mode):
    if mode == 1:
        username = "Swingeon"
        group_id = 11
        response = groups.join_group(user_id=2, group_id=group_id)

    elif mode == 2:
        username = "abcd"
        group_id = 11
        response = groups.join_group(user_id=2, group_id=group_id)

    elif mode == 3:
        username = "Swingeon"
        group_id = -1
        response = groups.join_group(user_id=2, group_id=group_id)

    print(response)


def test_leave_group(mode):
    if mode == 1:
        username = "Swingeon"
        group_id = 11
        response = groups.leave_group(user_id=2, group_id=group_id)

    elif mode == 2:
        username = "abcd"
        group_id = 11
        response = groups.leave_group(user_id=2, group_id=group_id)

    elif mode == 3:
        username = "Swingeon"
        group_id = -1
        response = groups.leave_group(user_id=2, group_id=group_id)

    print(response)


def test_search_groups(mode):
    if mode == 1:
        search_term = "hot"
        response = groups.search_groups(search_term)
        print(response)

    if mode == 2:
        search_term = "potato"
        response = groups.search_groups(search_term)
        print(response)


def test_load_group_members(mode):
    if mode == 1:
        group_id = 11
        response = groups.load_group_members(group_id)

