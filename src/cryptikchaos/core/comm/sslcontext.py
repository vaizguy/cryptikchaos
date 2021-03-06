'''
Created on Nov 16, 2013

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

from twisted.internet import ssl
from OpenSSL import SSL
from kivy import Logger

from cryptikchaos.exceptions.sslcontextExceptions import \
    SSLCertReadError, SSLKeyReadError
from cryptikchaos.core.env.configuration import constants


class TLSCtxFactory(ssl.ClientContextFactory):

    "Twisted SSL Context Factory."

    def __init__(self, crt, key, ca, postverify_hook):
        "Initializing SSL context"

        self.crt = crt
        self.key = key
        self.ca = ca
        self.postverify_hook = postverify_hook

    def getContext(self):
        "Get SSL context."

        # Now the options you can set Standard OpenSSL Library options

        # Selecting Transport Layer Security v1
        # The SSL protocol to use, one of SSLv23_METHOD, SSLv2_METHOD,
        # SSLv3_METHOD, TLSv1_METHOD. Defaults to TLSv1_METHOD.
        self.method = SSL.TLSv1_METHOD

        # If True, verify certificates received from the peer and fail
        # the handshake if verification fails. Otherwise, allow anonymous
        # sessions and sessions with certificates which fail validation.
        self.verify = True

        # Depth in certificate chain down to which to verify.
        self.verifyDepth = 1

        # If True, do not allow anonymous sessions.
        self.requireCertification = True

        # If True, do not re-verify the certificate on session resumption.
        self.verifyOnce = True

        # If True, generate a new key whenever ephemeral DH parameters are used
        # to prevent small subgroup attacks.
        self.enableSingleUseKeys = True

        # If True, set a session ID on each context. This allows a shortened
        # handshake to be used when a known client reconnects.
        self.enableSessions = True

        # If True, enable various non-spec protocol fixes for broken
        # SSL implementations.
        self.fixBrokenPeers = False

        # Get the client context factory
        ctx = ssl.ClientContextFactory.getContext(self)

        # Load certificate
        try:
            ctx.use_certificate_file(self.crt)

        except SSL.Error as exception:
            Logger.error("SSLCONTEXT: "+exception.message[0][2])
            raise SSLCertReadError(self.crt)

        else:
            Logger.info("SSLCONTEXT: Loaded Peer SSL Certificate.")

        # Load private key
        try:
            ctx.use_privatekey_file(self.key)

        except SSL.Error as exception:
            Logger.error("SSLCONTEXT"+exception.message[0][2])
            raise SSLKeyReadError(self.key)

        else:
            Logger.info("SSLCONTEXT: Loaded Peer SSL key.")

        # Set verify mode and verify callback chain.
        ctx.set_verify(
            SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
            self.verifyCallback
        )

        # Since we have self-signed certs we have to explicitly
        # tell the server to trust them.
        ctx.load_verify_locations(self.ca)

        return ctx

    def verifyCallback(self, connection, x509, errno, depth, preverifyOK):

        # default value of post verify is set False
        postverifyOK = False

        if not preverifyOK:
            # Pre-verification failed
            Logger.debug(
                "SSLCONTEXT: [Pre-verification] Certificate verification failed, {}".format(x509.get_subject()))

        else:
            # Add post verification callback here.
            # Get x509 subject
            subject = x509.get_subject()

            Logger.debug("SSLCONTEXT: [Pre-verification] Certificate [{}] Verfied.".format(subject))

            # Perform post verification checks
            postverifyOK = self.postverifyCallback(subject, preverifyOK)

            # Post verification tasks
            if postverifyOK:
                self.postverify_hook(connection, x509)

        return preverifyOK and postverifyOK

    def postverifyCallback(self, subject, preverifyOK):
        
        if not preverifyOK:
            return preverifyOK

        # variables for post-verify callback check on cert fields
        _cert_fields = constants.SSL_CERT_FIELDS
        _values_dict = constants.SSL_POST_VERIF_VALUES

        # Passed checks
        checklist_count = 0

        # Get certificate components
        certificate_components = dict(subject.get_components())

        # Check fields
        for i in _values_dict.keys():
            
            if certificate_components[_cert_fields[i]] in _values_dict[i]:
                checklist_count += 1
            else:
                print certificate_components[_cert_fields[i]] 
                print _values_dict[i]

        # Checklist roundoff
        if checklist_count == len(_values_dict.keys()):
            Logger.debug("SSLCONTEXT: [Post-verification] certificate verfication passed.")
            return True
        else:
            Logger.debug(
                "SSLCONTEXT: [Post-verification] Certificate verification failed. ({}/{} checks passed)".format(checklist_count, len(_values_dict.keys())))
            return False
