'''
Created on Oct 10, 2013

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

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

        # Error message
        if limit:
            self.stream_msg = "Exceeded limit of {} Bytes".format(
               limit
            )
        else:
            self.stream_msg = "Received stream does not match legal limits."

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
