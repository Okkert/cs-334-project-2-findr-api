from . import models
import smtplib
from .utils.toolbox import gen_response, gen_missing, debug_out, tattle, behaved
from .utils import response_constants as resp


# Function Status: Incomplete implementation, not tested
def load_notifications(user_id):
    """Loads all active notifications

    Parameters
    ----------
    user_id : int
        The ID of the user we want to load notifications for

    Returns
    -------
    dict
        JSON Response containing the notification payload

    """

    notes = models.load_notifications(user_id=user_id)
    if notes is False:
        return gen_missing("notifications")

    note_data = []
    for note in notes:
        note_data.append({
            "noteId": note.note_id,
            "userId": note.user_id,
            "status": note.note_status,
            "desc": note.note_desc,
            "time": note.note_birthday
        })

    content = {
        "notes": note_data
    }

    return gen_response(resp.OK, content)


# Function Status: Incomplete implementation, not tested
def create_note(note):
    """Creates an unread notification

    Parameters
    ----------
    note : dict
        <userId> : int
        <groupId> : int, optional
        <desc> : str
        <type> : int
    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        print(note)
        user_id = note["userId"]
        group_id = note["groupId"]
        subject_id = note["subjectId"]
        status = False
        desc = note["desc"]
        note_type = note["note_type"]
    except KeyError:
        print("params screwed up")
        return resp.RESP_INVALID

    if not models.user_exists(user_id):
        return gen_missing("user")

    if not models.group_exists(group_id):
        return gen_missing("group")

    valid = models.create_note(user_id=user_id, subject_id=subject_id, group_id=group_id, note_type=note_type, status=status,  desc=desc)
    if valid is False:
        content = {
            "reason": "Internal server error"
        }
        return resp.RESP_SERVER
    return resp.RESP_OK


# Function Status: Incomplete implementation, not tested
def delete_notification(note_id):
    """Deletes a notification

    Parameters
    ----------
    note_id : int

    Returns
    -------
    dict
        JSON Response detailing the success or failure of deleting the notification

    """
    status = models.delete_notification(note_id=note_id)
    if status is False:
        return gen_missing("notification")
    return resp.RESP_OK


# Function Status: Implemented, not tested
def update_notification(note_id):
    """Marks a notification as read

    Parameters
    ----------
    note_id : int

    Returns
    -------
    dict
        JSON Response detailing the success or failure of reading the notification

    """
    try:
        if not models.note_exists(note_id):
            return gen_missing("notification")

        success = models.update_notification(note_id)
        if success is False:
            return resp.RESP_SERVER
        return gen_response(resp.OK)
    except:
        return gen_response(resp.ERR_SERVER)


def load_notification(note_id):
    """Creates an unread notification

    Parameters
    ----------
    note_id : int
        Unique note identifier

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        n = models.load_notification(note_id)

        if n is None:
            return gen_missing("notification")

        note_data = {
            "noteId": n.note_id,
            "userId": n.user_id,
            "groupId": n.group_id,
            "status": n.note_status,
            "desc": n.note_desc,
            "time": n.note_birthday
        }

        content = {
            "note": note_data
        }

        return gen_response(resp.OK, content)
    except:
        return resp.RESP_SERVER


def construct_note(user_id, subject_id, group_id, note_type, desc):
    """Constructs a note dictionary

    Parameters
    ----------
    user_id : int
        Unique note identifier
    subject_id : int
        Identifier of the subject of the notification
    group_id : int
        Unique group identifier. Friendships go to group 69.
    note_type : str
        group/friend/dev
    desc : str
        Description of notification

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    note = {
        'userId': user_id,
        'subjectId': subject_id,
        'groupId': group_id,
        'note_type': note_type,
        'desc': desc
    }
    return note


def create_welcome_note(user_id):
    """Creates a welcome note

    Parameters
    ----------
    user_id : int
        Unique user identifier

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        note = construct_note(user_id, user_id, 69, 'dev', "Welcome to Findr!")
    except:
        print("create_welcome_note failed")
        return


def create_friend_request_note(user_id, friend_id):
    """Creates a welcome note

    Parameters
    ----------
    user_id : int
        Unique user identifier of the requestee
    friend_id : int
        Unique user identifier of the requested

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        user_a = models.search_user_by_id(user_id)
        msg = user_a.username + " would like to connect!"
        note = construct_note(friend_id, user_id, 69, 'friend', msg)
        create_note(note)
    except:
        print("create_friend_request_note failed")
        return


def create_friend_added_note(user_id, friend_id):
    """Notify users that their friendship is indeed magic

    Parameters
    ----------
    user_id : int
        Unique user identifier of the acceptor
    friend_id : int
        Unique user identifier of the accepted

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        user_a = models.search_user_by_id(user_id)
        user_b = models.search_user_by_id(friend_id)

        msg_a = "You and " + user_b.username + " have connected!"
        msg_b = "You and " + user_a.username + " have connected!"

        note = construct_note(user_id, friend_id, 69, 'friend', msg_a)
        create_note(note)
        note = construct_note(friend_id, user_id, 69, 'friend', msg_b)
        create_note(note)
    except:
        return resp.RESP_SERVER


def create_group_join_note(user_id, group_id):
    """Notifies group members of their new pal

    Parameters
    ----------
    user_id : int
        Unique user identifier
    group_id : int
        Unique group identifier
    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        u = models.search_user_by_id(user_id)
        g = models.search_group_by_id(group_id)

        if u is None:
            return gen_missing("User")

        # TODO: Get all members
        members = []
        msg = u.username + " joined " + g.group_name
        for member in members:
            note = construct_note(member.user_id, user_id, group_id, 'group', msg)
    except:
        return resp.RESP_SERVER



def create_group_request_note(user_id, group_id):
    """Notifies admins of a group join request

    Parameters
    ----------
    user_id : int
        Unique user identifier
    group_id : int
        Unique group identifier

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        group_name = group_id
        note = {
            'userId': user_id,
            'groupId': group_id,
            'note_type': "group",
            'desc': "A user has requested to join " + group_name
        }
        create_note(note)
    except:
        print("resolve_request_notification failed")
        return


def create_group_role_update(user_id, group_id, promoted):
    try:
        g = models.search_group_by_id(group_id)
        msg = "You've been "
        if promoted:
            msg += "promoted on"
        else:
            msg += "demoted on "
        msg += g.group_name
        note = construct_note(user_id, user_id, group_id, 'group', msg)
        create_note(note)
    except:
        print("create_group_role_update failed")


def create_group_request_resolved_note(user_id, group_id, was_accepted):
    """Notify user of their group request resolution

    Parameters
    ----------
    user_id : int
        Unique user identifier
    group_id : int
        Unique group identifier
    was_accepted : bool
        Indicates whether the request was accepted

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        group_name = group_id

        desc = "Your request to join " + group_name

        if was_accepted:
            desc += " was accepted!"
        else:
            desc += " was declined :("

        note = {
            'userId': user_id,
            'subjectId': user_id,
            'groupId': group_id,
            'note_type': "group",
            'desc': desc
        }
        create_note(note)
    except:
        print("create_request_resolved_notification failed")
        return


def update_group_request_notification(user_id, group_id, was_accepted):
    """Update an active group join request

    Parameters
    ----------
    user_id : int
        Unique user identifier
    group_id : int
        Unique group identifier
    was_accepted : bool
        Indicates whether the request was accepted or declined

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    try:
        # TODO: Find note with user_id and group_id
        # TODO: Delete note
        print("Implement update_group_request_notification pls")
    except:
        print("resolve_request_notification failed")
        return


# Function status: Implemented and tested
def send_registration_email(email, username):
    """Sends a registration email

    Parameters
    ----------
    email : str
        The email of the user registering for Findr
    username : str
        The username of the user registering for Findr
    """

    from_email = "noreply.findr@gmail.com"
    paprika = "hyhxnctegricdygd"
    subject = "Welcome to Findr!"
    body = f"Hey {username},\n\nThanks so much for singing up to Findr!\nWe couldn't be " \
           f"more thankful that you chose Findr to unite yourself and your loved ones with the broader " \
           f"polyamorous community filled with like minded people.\n\nRemember, don't be shy. If " \
           f"you like what you see, don't be afraid to reach out couples, because here at Findr " \
           f"we believe that there's always room for one more.\n\n" \
           f"All the best,\nThe Findr Team"

    msg = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(user=from_email, password=paprika)
        connection.sendmail(from_addr=from_email, to_addrs=email, msg=msg)
        connection.close()


# Function status: Not implemented correctly
def send_password_retrieval_email(email, username, cumin):
    """Sends a password retrieval email

    Parameters
    ----------
    email : str
        The email of the user who forgot their password
    username : str
        The username of the user who forgot their password
    cumin: str
        The password of the user
    """

    from_email = "noreply.findr@gmail.com"
    paprika = "hyhxnctegricdygd"
    subject = "Forgot your password?"
    body = f"Hey {username},\n\nIt seems like you forgot your password. Here's a little reminder of " \
           f"your findr account details:\n\nUsername: {username}\nPassword: {cumin}\n\n.All the best,\nThe Findr Team"
    msg = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(user=from_email, password=paprika)
        connection.sendmail(from_addr=from_email, to_addrs=email, msg=msg)
        connection.close()


