#  -  -  -  -  -  -  #
# CS 314 - Project 3 #
#  -  -  -  -  -  -  #
# toolbox.py
# Auxilary functions

from rest_framework.response import Response

# Constants
DEBUG = True


# Functions
def debug_out(msg):
    """Print debug message

        Parameters
        -------
        msg : str
            Message to print
    """
    if DEBUG:
        print(msg)
    return


def gen_response(status, data=None):
    """Generates a custom response as a python dictionary

        Parameters
        -------
        status : int
            Response status code

        data : dict
            Object of response content

        Returns
        -------
        dict
            Dictionary version of final response
    """
    #response = {
    #    "status": status,
    #    "content": content
    #}
    #debug_out(response)
    return Response(status=status, data=data)


def gen_missing(lost_item):
    msg = "Failed to find " + lost_item
    return Response(status=404, data={"reason": msg})


# NOTE:
# tattle() and behaved() are used to check a list of requirements (validation)
# if we tattle() each of the requirements, behaved() will tell us if any of them failed
# and the string we use as 'board' will store the first error message so that we can output the error message later.


# SIDENOTE:
# behaved() is just one line, but I don't think tattle() would be complete without it. I just liked the theme/names.


def tattle(event, reason, board):
    """Evaluates event and if something goes wrong writes the reason on the board

        Parameters
        -------
        event : bool
            Event is TRUE if it succeeds, FALSE otherwise

        reason : str
            Reason for failure

        board : str
            Teacher stores reason, in case of failure
    """
    if not event:
        if len(board) == 0:
            board = reason
    return board


def behaved(board):
    """Checks whether the board has any failures logged
        Parameters
        -------
        board : str
            A string of the first noted failure in a process

        Returns
        -------
        bool
            FALSE if any failures were noted on the board, TRUE otherwise
    """
    return len(board) == 0

