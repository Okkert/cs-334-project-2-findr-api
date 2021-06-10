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
def create_notification(note):
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
        user_id = note["userId"]
        status = False
        desc = note["desc"]
        note_type = note["note_type"]
        group_id = note["groupId"]
    except KeyError:
        return resp.RESP_INVALID

    status = models.create_notification(user_id=user_id, status=status, note_type=note_type, desc=desc, group_id=group_id)
    if status is False:
        content = {
            "reason": "Internal server error"
        }
        return resp.RESP_SERVER

    content = {
        "reason": "Note created"
    }
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
        status = models.update_notification(note_id)
        if status is False:
            content = {
                "reason": "Internal server error"
            }
            return gen_response(resp.ERR_SERVER, content)
        return gen_response(resp.OK)
    except:
        return gen_response(resp.ERR_SERVER, content)


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
        n = load_notification(note_id)

        if n is None:
            return gen_missing("notification")

        note_data = {
            "noteId": n.note_id,
            "userId": n.user_id,
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


