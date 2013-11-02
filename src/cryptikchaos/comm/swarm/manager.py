'''
Created on Aug 3, 2013

Peer manager is used to Handle the peer information.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from cryptikchaos.comm.swarm.peer import Peer
from cryptikchaos.config.configuration import constants

from cryptikchaos.libs.utilities import random_color_code

from kivy.logger import Logger

import shelve


class SwarmManager:
    "Manage peers in the swarm."

    def __init__(self, peerid, peerkey):

        peerfile = "{}/db/{}_db".format(
            constants.PROJECT_PATH,
            peerid
        )

        self.my_peerid = peerid
        self.my_key = peerkey
        self.my_msg_rcc = random_color_code()

        self._peer_dict = shelve.open(
            peerfile,
            flag='c',
            protocol=None,
            writeback=True
        )

        self.peer_connections = {}

    def __del__(self):

        # Closing all connections
        Logger.info("Closing all connections.")
        
        peer_ids = self.list_peer_ids()
        
        # Exit if no connections to clear
        if not peer_ids:
            return None
        
        # Remove peer connections
        for pid in peer_ids:
            # Update peer connection status
            self.update_peer_connection_status(pid, False)
            # Remove existing connection objects
            self.peer_connections[pid] = None

        # Close peer dict if it exists
        self._peer_dict.close()

    def add_peer(self, pid, key, host, port):
        "Add peer to database."

        # localhost - 127.0.0.1 mapping.
        if host == "localhost":
            host = constants.LOCAL_TEST_HOST

        Logger.debug("Adding Peer {} , {}@{}".format(pid, host, port))

        if str(pid) in self._peer_dict:
            Logger.warn("Peer {} already exists. No changes made.".format(pid))
            return None
        else:
            Logger.debug("Adding Peer {} , {}@{}".format(pid, host, port))
            
        # Random message color code
        while True:
            # Get RCC
            rcc = random_color_code()
            # Check if color not used
            if rcc not in self.list_peer_id_colors():
                break                

        # Peer dictionary structure defined here
        self._peer_dict[str(pid)] = Peer({
            "PEER_ID": pid,
            "PEER_KEY" : key,
            "PEER_IP": host,
            "PEER_PORT": port,
            "PEER_CONN_STATUS": False,
            "PEER_ID_COLOR" : rcc
        })

        # Sync DB
        self._peer_dict.sync()

    def delete_peer(self, pid):
        "Remove unauth peer."

        del self._peer_dict[str(pid)]
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
                "Invalid Peer Connection Status, must be True or False."
            )

    def list_peer_ids(self):
        "Returns a list of all peer IDs present in swarm."
        
        try:
            return self._peer_dict.keys()
        except AttributeError:
            return []

    def build_swarm_graph(self):
        "Return visual graph of entire swarm."

        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except ImportError:
            Logger.error("Requires Networkx & Matplotlib modules.")
            return False
        else:
            # Create graph
            swarm_graph = nx.Graph()

            # Populate graph
            for pid in self.list_peer_ids():
                swarm_graph.add_edge(self.my_peerid, pid)

            # Plot circular graph
            nx.draw_circular(swarm_graph)

            # Show graph plot
            plt.show()

            return True

    def list_peers(self):
        "Returns a list of all the peers."

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
    
    def list_peer_id_colors(self):
        "Returns a list of all the peers."

        rcclist = []

        for k in self._peer_dict.keys():
            # Get peer attributes/
            p_info = self._peer_dict[k]
            # Append id rcc
            rcclist.append(
                p_info["PEER_ID_COLOR"],
            )

        return rcclist
    
    def list_live_peers(self):
        "Returns a list of all online peers."

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

    ## Need to simplify mapping TODO
    def get_peerid_from_ip(self, peer_ip, peer_port=constants.PEER_PORT):
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
        "Get the peers key."

        if str(pid) in self._peer_dict.keys():
            return self._peer_dict[str(pid)]["PEER_KEY"]
        else:
            return None
        
    def get_peerid_color(self, pid):
        "Return peer's color code."
        
        if str(pid) in self._peer_dict.keys():
            return self._peer_dict[str(pid)]["PEER_ID_COLOR"]
        else:
            return self.my_msg_rcc
        
    def is_peer(self, pid):
        "Check if peer got added successfully."
        
        if str(pid) in self._peer_dict:
            return True
        else:
            return False

if __name__ == '__main__':
    pm = SwarmManager("{}/db/test_peerlist_db".format(
        constants.PROJECT_PATH
    ))
    pm.add_peer(123, 'localhost', 8000)
    pm.add_peer(234, 'localhost', 8001)
    pm.add_peer(345, 'localhost', 8002)
    pm.add_peer(456, 'localhost', 8003)
    print pm.list_peers()
