'''
Created on Oct 10, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

from cryptikchaos.core.env.configuration import constants


class StreamError(Exception):
    pass


class StreamOverflowError(StreamError):

    """
    If capsule unpack fails.
    """

    def __init__(self, limit=None):

        # Size limit
        if limit:
            self.limit = constants.STREAM_SIZE
        else:
            self.limit = limit

        # Error message
        self.stream_msg = "Exceeded limit of {} Bytes".format(
            self.limit
        )

        # Content information
        self.info = "Message limit is capped at {}.".format(
            constants.STREAM_CONTENT_LEN)

    def __str__(self):

        return self.stream_msg


class StreamEmptyError(StreamError):

    """
    If capsule is empty.
    """

    def __init__(self):

        pass

    def __str__(self):

        return "Stream not populated with data."


if __name__ == "__main__":

    raise StreamOverflowError()
