from django.test import TestCase
# The imports below cause errors for me for some reason
# from . import groups
# from . import posts
import findr.app.posts as posts
import findr.app.groups as groups
import findr.app.auth as auth


# ---------------------------- POSTS TESTS ------------------------------- #
def test_create_post(mode, group_id, user_id):
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
            "groupId": group_id,
            "author": {
                "userId": user_id,
                "username": "Swingeon\n",
                "avatar": "path/to/jane42.png\n"
            },
            "title": "Test 1",
            "postContent": "Description 1",
            "location": "Stellenbosch",
            "category": "Hot"
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


def test_edit_post(mode):
    if mode == 1:
        post = {
            "postId": 1,
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
        response = posts.like_post(1, 2)
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
        posts.post_comment(1, comment)
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


def test_load_post(mode):
    if mode == 1:
        response = posts.load_post(1)
    if mode == 2:
        response = posts.load_post(-1)


# ---------------------------- GROUP TESTS ------------------------------- #
def test_create_group(mode, user_id):
    """Tests create_group()

    Parameters
    ----------
    mode : int
        If mode is 1 it tests a legitimate create group, 2 tests a bad request
    """

    if mode == 1:
        group = {
            "title": "Bush Babies",
            "desc": "I like limas, bats and bush babies\n",
            "private": False
        }

    if mode == 2:
        group = {
            "title": "Jane's Hot Tub Party",
        }

    response = groups.create_group(group, user_id)


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


# TODO: Add more testing modes
def test_edit_group(mode):
    """Tests edit_group()

    Parameters
    ----------
    mode : int
        If mode is 1 it tests load_group() by group name, if mode is 2 it tests load_group()
        by id, if mode is 3 it tests with a non-existent group and if mode is 4 it tests a bad request
    """
    if mode == 1:
        group = {
            "id": 14,
            "title": "Suzie's Thruple",
            "desc": "Just me, Steve and Swingeon",
            "private": True
        }
        response = groups.edit_group(group)


def test_join_group(mode, group_id, user_id):
    if mode == 1:
        response = groups.join_group(user_id=user_id, group_id=group_id)

    elif mode == 2:
        group_id = 18
        response = groups.join_group(user_id=-1, group_id=group_id)

    elif mode == 3:
        group_id = -1
        response = groups.join_group(user_id=user_id, group_id=-1)


def test_leave_group(mode, group_id, user_id):
    if mode == 1:
        response = groups.leave_group(user_id=user_id, group_id=group_id)

    elif mode == 2:
        group_id = 13
        response = groups.leave_group(user_id=user_id, group_id=group_id)

    elif mode == 3:
        group_id = -1
        response = groups.leave_group(user_id=user_id, group_id=group_id)


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
        group_id = 18
        response = groups.load_group_members(group_id)
    if mode == 2:
        group_id = -1
        response = groups.load_group_members(group_id)


def test_load_group_posts(mode, group_id):
    if mode == 1:
        groups.load_group_posts(group_id)
    elif mode == 2:
        groups.load_group_posts(-1)


def test_promote_member(mode, user_id, group_id):
    if mode == 1:
        groups.promote_member(group_id=group_id, user_id=2, promote_user_id=user_id)
    if mode == 2:
        groups.promote_member(group_id=-1, user_id=2, promote_user_id=user_id)
    if mode == 3:
        groups.promote_member(group_id=group_id, user_id=3, promote_user_id=user_id)
    if mode == 4:
        groups.promote_member(group_id=group_id, user_id=2, promote_user_id=-1)


def test_demote_member(mode, group_id, user_id):
    if mode == 1:
        groups.demote_member(group_id=group_id, user_id=2, demote_user_id=user_id)
    if mode == 2:
        groups.demote_member(group_id=-1, user_id=2, demote_user_id=user_id)
    if mode == 3:
        groups.demote_member(group_id=group_id, user_id=3, demote_user_id=user_id)
    if mode == 4:
        groups.demote_member(group_id=group_id, user_id=2, demote_user_id=-1)


def test_load_join_request(mode, group_id):
    if mode == 1:
        groups.load_join_request(group_id=group_id)


def test_request_group_invite(mode, group_id, user_id):
    if mode == 1:
        groups.request_group_invite(group_id=group_id, user_id=user_id)
    if mode == 2:
        groups.request_group_invite(group_id=-1, user_id=user_id)
    if mode == 3:
        groups.request_group_invite(group_id=group_id, user_id=-1)


def test_accept_join_request(mode, group_id, user_id):
    if mode == 1:
        groups.accept_join_request(group_id=group_id, user_id=user_id)
    if mode == 2:
        groups.accept_join_request(group_id=-1, user_id=user_id)
    if mode == 3:
        groups.accept_join_request(group_id=group_id, user_id=-1)


def test_decline_join_request(mode, group_id, user_id):
    if mode == 1:
        groups.decline_join_request(group_id=group_id, user_id=user_id)
    if mode == 2:
        groups.decline_join_request(group_id=-1, user_id=user_id)
    if mode == 3:
        groups.decline_join_request(group_id=group_id, user_id=-1)


# ---------------------------- NOTIFICATION TESTS ------------------------------- #

# TODO
def test_load_notification():
    return True


# TODO
def test_create_notification():
    return True


# TODO
def test_delete_notification():
    return True


# TODO
def test_update_notification():
    return True


# ---------------------------- FEED TESTS ------------------------------- #
# TODO
