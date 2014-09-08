'''
Created on Nov 17, 2013

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


class SSLContextError(Exception):
    pass


class SSLCertReadError(SSLContextError):

    def __init__(self, path):

        self.msg = """
            Missing SSL Certificate / Key
            -----------------------------

            Please place a valid SSL certificate in
            {}
            (OR)
            Change configuration variable constants.ENABLE_TLS* to False.

            *TLS mode is still in experimental phase.
        """.format(path)

    def __str__(self):

        return self.msg


class SSLKeyReadError(SSLContextError):

    def __init__(self, path):

        self.msg = """
            Missing SSL Certificate / Key
            -----------------------------

            Please generate a valid SSL certificate in
            {}
            (OR)
            Change configuration variable constants.ENABLE_TLS* to False.

            *TLS mode is still in experimental phase.
        """.format(path)

    def __str__(self):

        return self.msg
