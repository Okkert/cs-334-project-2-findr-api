from findr.app.auth import register, login, logout
from findr.app.utils.toolbox import debug_out, tattle, behaved
from findr.app.utils import response_constants as resp
from findr.app import notes

username = "Dummy321"
email = "dummy@fakemail.com"
password = "FooBar1234567890!@"
token = ""
board = ""


# TODO: Add query for removing user, otherwise this test will only run once then fail on the second execution due to duplicate username


def ok(response):
    return response['status'] == resp.OK


def test_register():
    resp_a = register(username, email, password)
    resp_b = register(username, email, password)

    tattle(ok(resp_a), "Failed to register", board)
    tattle(not ok(resp_b), "Registered duplicate", board)


def test_login_username():
    resp_a = login(username, None, password, True)

    if 'token' in resp_a['content']:
        resp_b = logout(resp_a['content']['token'])
        tattle(ok(resp_b), "Failed to logout", board)
    else:
        tattle(False, "Failed to logout", board)


def test_false_logout():
    resp_a = logout("foo")
    tattle(not ok(resp_a), "Logged out with invalid token", board)


def test_login_email():
    resp_a = login(None, email, password, True)

    if 'token' in resp_a['content']:
        resp_b = logout(resp_a['content']['token'])
        tattle(ok(resp_b), "Failed to logout", board)
    else:
        tattle(False, "Failed to logout", board)


def test_auth():
    debug_out("Testing authentication")
    test_register()
    test_login_username()
    test_login_email()
    test_false_logout()
    if behaved(board):
        debug_out("Auth Test Success!")
    else:
        debug_out(board)


print(notes.create_notification(
    {
        "userId": 1,
        "groupId": 1,
        "desc": "You have a friend invite!",
        "note_type": 1
    }))

