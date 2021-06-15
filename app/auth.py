#  -  -  -  -  -  -  #
# CS 314 - Project 3 #
#  -  -  -  -  -  -  #
# auth.py
# Authentication management

# FIXME: Import paths are a bit weird here
import csv
import re
import smtplib

from passlib.handlers.sha2_crypt import sha256_crypt

from .utils.toolbox import gen_response, debug_out, tattle, behaved
from .utils import response_constants as resp
from rest_framework import authentication
from . import models, notes
import jwt
import datetime
import random

# This is the salt used for hashing, but we call it pepper so that hackers can't find it as easily
PEPPER = "dLO\\x8e\\x90\\xa1\\xc2D\\xf6&[\\xc6\\x165\\xf5\\x84b\\xc9\\x99\\xa4\\xa8\\xf7VQ"
TOKEN_HUH = -1
TOKEN_INVALID = -2
TOKEN_EXPIRED = -3
MINUTES_IN_MONTH = 43800

# Auxilary functions


def get_request_token(headers):
    try:
        if 'Authorization' in headers:
            auth = headers['Authorization']
            token_str = auth.split(" ")
            token = token_str[1]
            print("Got token ", token)
            return token
        else:
            print("No Authorization sent")
            return None
    except:
        print('get_request_token failed')
        return None


def decode_token(token):
    """ Decodes a token and returns the token owner's user_id

    Parameters
    ----------
    token : string
        Authentication token to decode
    Returns
    -------
    int
        Token owner's user id, -1 if token is invalid
    """
    try:
        payload = jwt.decode(token, PEPPER, algorithms='HS256')
        user_id = payload['sub']
        print("token decoded: ", user_id)
        return user_id
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        print("Token invalid")
        return TOKEN_INVALID
    except:
        print("Token weird")
        return TOKEN_HUH

# Auth functions


#  -  -  -  #
#  Tokens   #
#  -  -  -  #

def gen_token(user_id, password, expire):
    """ Generates a new token and stores it in the database

    Parameters
    ----------
    user_id : int
        The id of the user to receives the generated token. Added to token payload
    password : str
        Password of the user - to prevent other uses from generating tokens for them
    expire : bool
        Indicates whether a token should expire

    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation

    """
    try:
        # Set token expiry date
        expire_time = datetime.timedelta(minutes=30)
        if not expire:
            expire_time = datetime.timedelta(minutes=MINUTES_IN_MONTH)

        # TODO: Remove route for gen auth token, it only matters for login
        # Check if password is valid to prevent anyone from overwriting your token
        #db_user = models.search_user(user_id)

        #if not sha256_crypt.verify(password, db_user.password):
        #    return gen_response(resp.ERR_UNAUTH, {"reason": "Incorrect password"})

        # Generate token
        payload = {
            'exp': datetime.datetime.utcnow() + expire_time,
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(payload, PEPPER, algorithm='HS256')

        query_success = models.store_token(user_id, token)

        # Prepare response
        if query_success:
            return token #gen_response(resp.OK, {"token": token})
        else:
            return None #gen_response(resp.ERR_MISSING, {})
    except:
        debug_out("gen_token failed")
        return gen_response(resp.ERR_SERVER, {})


def destroy_token(token):
    """ Revokes an existing auth token's validity

    Parameters
    ----------
    token : int
        The encrypted authentication token
    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation

    """
    try:
        user_id = decode_token(token)

        # Invalid tokens
        if user_id == -1:
            return gen_response(resp.ERR_INVALID, {"reason": "Invalid auth token"})

        query_success = models.remove_token(user_id, token)

        if query_success:
            return gen_response(resp.OK, {})
        else:
            return gen_response(resp.ERR_MISSING, {"reason": "Failed to find user"})
    except:
        content = {
            "reason": "Unexpected error occurred"
        }
        return gen_response(resp.ERR_SERVER, content)


def confirm_token(token):
    """ Confirms token validity

    Parameters
    ----------
    token : int
        The encrypted authentication token
    Returns
    -------
    dict
        JSON Response detailing the success or failure of operation

    """
    try:
        user_id = decode_token(token)

        # Invalid tokens
        if user_id < 0:
            content = {
                "reason": "Unexpected server error"
            }
            if user_id == TOKEN_EXPIRED:
                content['reason'] = "Token has expired, please log in again"
            elif user_id == TOKEN_INVALID:
                content['reason'] = "Invalid token"
            return gen_response(resp.ERR_INVALID, content)

        db_token = models.fetch_token(user_id)
        query_success = True
        if db_token is None:
            query_success = False

        if query_success:
            # Validate token vs database token
            if bytes(token, encoding="utf8") != bytes(db_token, encoding="utf8"):
                return gen_response(resp.ERR_INVALID, {"reason": "Invalid auth token"})
            else:
                return gen_response(resp.OK, {})
        else:
            return gen_response(resp.ERR_MISSING, {"reason": "Failed to find user"})
    except:
        debug_out("Failed to confirm token")
        return gen_response(resp.ERR_SERVER, {})


def gen_cool_code():

    with open('adjectives.csv', newline='') as fa:
        reader = csv.reader(fa)
        data = list(reader)
        adjectives = data

    with open('food.csv', newline='') as fo:
        reader = csv.reader(fo)
        data = list(reader)
        foods = data


    adj = random.choice(adjectives[0])
    food = random.choice(foods[0])
    number = random.randint(10, 99)
    code = adj + "-" + food + "-" + str(number)
    return code


#  -  -  -  -  #
# Validation   #
#  -  -  -  -  #

def valid_password(password):
    """Validates password

        Returns
        -------
        bool
            TRUE if password is valid, FALSE otherwise.
        """
    try:
        pass_valid = re.search("^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*\\W).{12,}$", password)
        return pass_valid is not None
    except:
        debug_out("valid_password failed")
        return False


def valid_email(email):
    """Validates email

        Returns
        -------
        bool
            TRUE if email is valid, FALSE otherwise.
        """
    try:
        email_valid = re.search(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email)
        valid = email_valid is not None
        return valid and not email_exists(email)
    except:
        debug_out("valid_email failed")
        return False


def username_exists(username):
    """Checks if a username exists

            Returns
            -------
            bool
                TRUE if username is valid, FALSE otherwise.
            """
    try:
        user = models.search_username(username)
        return user is not None
    except:
        debug_out("valid_username failed")
        return False


def user_exists_and_valid(user_id):
    try:
        test = int(user_id)
        user = models.search_user_by_id(user_id)
        return user is not None
    except:
        return False


def email_exists(email):
    try:
        user = models.search_user_email(email)
        return user is not None
    except:
        debug_out("email_exists failed")
        return False


#  -  -  -  -  -  #
#  Login/Register #
#  -  -  -  -  -  #

def register(username, email, password):
    """Attempts to register user

        Parameters
        ----------
        username : str
            Unique username
        email : str
            User's email
        password : str
            User's password, right now it doesn't have to be hashed

        Returns
        -------
        dict
            JSON Response detailing the success or failure of operation
    """
    try:
        board = ""
        valid_username = not username_exists(username)
        board = tattle(valid_username, "Invalid username", board)
        board = tattle(valid_email(email), "Invalid email", board)
        board = tattle(valid_password(password), "Invalid password", board)

        hash_pass = sha256_crypt.encrypt(password)

        if behaved(board):
            models.insert_user(username, email, hash_pass)
            response = gen_response(resp.OK, {})

            u = models.search_username(username)

            # Notifications + Email Verification
            try:
                verify_code = gen_cool_code()
                u.auth_token = "email " + verify_code
                send_registration_email(email, username, verify_code)
                # notes.create_welcome_note(u.user_id)
            except:
                print("Notifications on register failed")
        else:
            response = gen_response(resp.ERR_INVALID, {"reason": board})
        return response
    except:
        debug_out("register failed")
        return gen_response(resp.ERR_SERVER, None)


def login(username, email, password, remember_me):
    """Attempts to log user in

        Parameters
        ----------
        username : str
            User's account username (optional, if email entered)
        email : str
            User's account email (optional, if username entered)
        password : str
            User's account password (not hashed)
        remember_me : bool
            If true - tokens will not expire, Else - tokens expire in 30 minutes
        Returns
        -------
        dict
            JSON Response detailing the success or failure of operation
    """
    try:
        user = None
        if username is not None:
            if username_exists(username):
                user = models.search_username(username)
            else:
                response = gen_response(resp.ERR_INVALID, {"reason": "Invalid username"})
                return response
        elif email is not None:
            user = models.search_user_email(email)
        else:
            return gen_response(resp.ERR_INVALID, {"reason": "Username and email can't both be empty"})

        # Validate query response
        if user is None:
            return gen_response(resp.ERR_MISSING, {"reason": "Failed to find user"})

        # Check verified account
        #if user.auth_token is not None:
        #    if user.auth_token.startswith("email"):
        #       return gen_response(resp.RESP_INVALID, {"reason:" "You need to verify your account first"})

        # Verify password
        if sha256_crypt.verify(password, user.password):
            token_resp = gen_token(user.user_id, password, not remember_me)
            data = {
                'token': token_resp,
                'user_id': user.user_id
            }
            return gen_response(resp.OK, data)
        else:
            return gen_response(resp.ERR_INVALID, {"reason": "Invalid password"})
    except:
        debug_out("login failed")
        return gen_response(resp.ERR_SERVER, None)


def logout(token):
    """Attempts to log user out

        Parameters
        ----------
        token : str
            User's authentication token

        Returns
        -------
        dict
            JSON Response detailing the success or failure of operation
    """
    try:
        user_id = decode_token(token)

        reason = ""
        if user_id == TOKEN_EXPIRED:
            reason = "Token has expired"

        if user_id == TOKEN_INVALID:
            reason = "Token is invalid"

        if user_id == TOKEN_HUH:
            reason = "Unknown token error"

        if len(reason) != 0:
            return gen_response(resp.ERR_UNAUTH, {"reason": reason})

        user = models.search_user(user_id)

        # TODO: !!! MATCH USER TOKEN TO GIVEN TOKEN !!!

        if user is None:
            return gen_response(resp.ERR_MISSING, {"reason": "Failed to find user"})

        remove_success = models.remove_token(user_id, token)

        if remove_success:
            return gen_response(resp.OK, None)
        else:
            return gen_response(resp.ERR_INVALID, {"reason": "Failed to remove token"})

    except:
        debug_out("logout failed")
        return gen_response(resp.ERR_SERVER, None)


# Function status: Implemented and tested
def send_registration_email(email, username, code):
    """Sends a registration email

    Parameters
    ----------
    email : str
        The email of the user registering for Findr
    username : str
        The username of the user registering for Findr
    code : str
        Email verification code
    """
    print(code)
    from_email = "noreply.findr@gmail.com"
    paprika = "hyhxnctegricdygd"
    subject = "Welcome to Findr!"
    body = f"Hey {username},\n\nWelcome to Findr!\nYou're only one step away from meeting the loves of your life" \
           f" or sharing your passion for hot tubs.\n\nYour email verification code is: {code}\n\n" \
           f"Have fun and remember: Talk to strangers!\n\nxoxo\n\nThe Findr Team"

    msg = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(user=from_email, password=paprika)
        connection.sendmail(from_addr=from_email, to_addrs=email, msg=msg)
        connection.close()


