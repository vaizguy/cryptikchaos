'''
Created on Aug 3, 2013

Peer manager is used to Handle the peer information.

@author: vaizguy
'''
from cryptikchaos.comm.peers.peer import Peer
from cryptikchaos.config.configuration import *

from kivy.logger import Logger

import shelve

__author__ = "Arun Vaidya"
__version__ = 0.1


class PeerManager:

    def __init__(self, peerid, peerkey):
        
        peerfile = constants.PROJECT_PATH + "/db/"+ str(peerid) +"_db"
        
        self.my_peerid = peerid
        self.my_key = peerkey

        self._peer_dict = shelve.open(
            peerfile,
            flag='c',
            protocol=None,
            writeback=True)

        ## Add test server
        self.add_peer(pid=constants.LOCAL_TEST_PEER_ID, 
                      key=constants.LOCAL_TEST_SERVER_KEY,
                      host=constants.LOCAL_TEST_HOST,
                      port=constants.LOCAL_TEST_PORT
                      )

        self.peer_connections = {}

    def __del__(self):

        self._peer_dict.close()

    def add_peer(self, pid, key, host, port):
        "Add peer to database."

        # localhost - 127.0.0.1 mapping.
        if host == "localhost":
            host = constants.LOCAL_TEST_HOST

        Logger.debug("Adding Peer {} , {}@{}".format(pid, host, port))

        # Peer dictionary structure defined here
        self._peer_dict[str(pid)] = Peer({
            "PEER_ID": pid,
            "PEER_KEY" : key,
            "PEER_IP": host,
            "PEER_PORT": port,
            "PEER_CONN_STATUS": False,
        })

        # Sync DB
        self._peer_dict.sync()

    def get_peer(self, pid):
        "Get peer from db."

        if str(pid) in self._peer_dict.keys():
            return self._peer_dict[str(pid)]
        else:
            return None

    def add_peer_connection(self, pid, conn):
        "Add a peer connection."

        try:
            self.peer_connections[pid] = conn
        except KeyError:
            Logger.error("Invalid Peer ID.")
            return False
        else:
            return True

    def connect_to_peer(self, pid):
        "Get stored peer connection from pid."

        try:
            stat = self.get_peer_connection_status(pid)
        except KeyError:
            Logger.error("Invalid Peer ID.")
            return None
        else:
            if stat:
                return self.get_peer_connection(pid)
            else:
                return None

    def update_peer_connection_status(self, pid, status):
        "Update peer's connection status."

        if status in (True, False):
            # Set new connection status
            self._peer_dict[str(pid)]["PEER_CONN_STATUS"] = status
            # Sync DB
            self._peer_dict.sync()
        else:
            raise Exception(
                "Invalid Peer Connection Status, must be True or False.")

    def list_peers(self):
        "Returns a list of all the peers"

        peerlist = []

        for k in self._peer_dict.keys():
            # Get peer attributes/
            p_info = self._peer_dict[k]
            # Append as tuples (peer id, peer host, peer port, peer status)
            peerlist.append(
                (p_info["PEER_ID"],
                 p_info["PEER_KEY"][0:3] + "XXXX",
                 p_info["PEER_IP"],
                 p_info["PEER_PORT"],
                 p_info["PEER_CONN_STATUS"]))

        return peerlist

    def list_live_peers(self):
        "Returns a list of all online peers"

        peerlist = []

        for k in self._peer_dict.keys():
            # Get peer attributes
            p_info = self._peer_dict[k]

            if self.get_peer_connection_status(k):
                # Append as tuples (peer id, peer host, peer port, peer status)
                peerlist.append(
                    (p_info["PEER_ID"],
                     p_info["PEER_KEY"][0:3] + "XXXX",
                     p_info["PEER_IP"],
                     p_info["PEER_PORT"],
                     p_info["PEER_CONN_STATUS"]))

        return peerlist

    def peer_host(self, pid):
        "Returns a peer's IPv4 address."

        return self._peer_dict[str(pid)]["PEER_IP"]

    def get_peerid_from_ip(self, peer_ip, peer_port=8000):
        "Get a peerid from stored IP addresses. Assumes 1to1 relation."

        for (pid, _, ip, port, _) in self.list_peers():
            if ip == peer_ip and port == peer_port:
                return int(pid)

        return None  # Add relevent catch

    def get_peer_connection_status(self, pid):
        "Get the peer connection status."

        if str(pid) in self._peer_dict.keys():
            return self._peer_dict[str(pid)]["PEER_CONN_STATUS"]
        else:
            return False

    def get_peer_connection(self, pid):
        "Get the peer connection."

        return self.peer_connections[pid]
    
    def get_peer_key(self, pid):
        "Get the peers key"
        
        if str(pid) in self._peer_dict.keys():
            return self._peer_dict[str(pid)]["PEER_KEY"]
        else:
            return None


if __name__ == '__main__':
    pm = PeerManager(constants.PROJECT_PATH + "/db/test_peerlist_db")
    pm.add_peer(123, 'localhost', 8000)
    pm.add_peer(234, 'localhost', 8001)
    pm.add_peer(345, 'localhost', 8002)
    pm.add_peer(456, 'localhost', 8003)
    print pm.list_peers()
