from . import models
import smtplib
from .utils.toolbox import gen_response, debug_out, tattle, behaved
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
    content = {
        "noteId": 1,
        "userId": 42,
        "status": True,
        "desc": "PretorisaurusRexxx would like to connect!\n",
        "time": "01:02:03 04/05/2006\n"
    }

    return gen_response(resp.OK, content)


# Function Status: Incomplete implementation, not tested
def create_notification(note):
    """Creates an unread notification

    Parameters
    ----------
    note : dict
        <user_id> : int
        <status> : boolean
        <desc> : str

    Returns
    -------
    dict
        JSON Response detailing the success or failure of notification creation

    """
    content = {
        "reason": "Note created"
    }
    return gen_response(resp.OK, content)


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
    content = {
        "reason": "Note deleted"
    }
    return gen_response(resp.OK, content)


# Function Status: Incomplete implementation, not tested
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
    content = {
        "reason": "Note read"
    }
    return gen_response(resp.OK, content)


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
