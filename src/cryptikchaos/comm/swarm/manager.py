'''
Created on Aug 3, 2013

Peer manager is used to Handle the peer information.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from cryptikchaos.libs.Storage.manager import StoreManager

from cryptikchaos.env.configuration import constants

from cryptikchaos.comm.swarm.peer import Peer

from kivy.logger import Logger

if constants.NETWORKX_AVAILABLE:
    import networkx as nx
    import matplotlib.pyplot as plt
    
class SwarmManager(StoreManager):
    "Manage peers in the swarm."

    def __init__(self, peerid, peerkey):
       
        # Authorized keys
        self._valid_keys = (
            "PEER_ID", "PEER_KEY", "PEER_IP", "PEER_PORT", \
            "PEER_STATUS", "PEER_COLOR"
        )
        
        # Create store
        super(SwarmManager, self).__init__(
            "{}_SwarmStore".format(peerid), 
            self._valid_keys, 
        )

        # Client Attributes
        self.my_peerid = peerid
        self.my_key = peerkey
        self.my_msg_rcc = peerid

        # Hold peer commections
        self.peer_connections = {}
        # Hold peer pending streams
        self.peer_stream_buffer = {}
        
        # Create graph
        if constants.NETWORKX_AVAILABLE:
            self.swarm_graph = nx.Graph()

    def __del__(self):
        
        peer_ids = self.list_peer_ids()
        
        # Exit if no connections to clear
        if peer_ids:       
            # Remove peer connections
            for pid in peer_ids:
                # Delete peer
                self.delete_peer(pid)
           
        # Close store 
        StoreManager.__del__(self)

    def add_peer(self, pid, key, host, port):
        "Add peer to database."

        # localhost - 127.0.0.1 mapping.
        if host == "localhost":
            host = constants.LOCAL_TEST_HOST

        Logger.debug("Adding Peer {} , {}@{}".format(pid, host, port))

        if pid in self.keys():
            Logger.warn("Peer {} already exists. No changes made.".format(pid))
            return None
        else:
            Logger.debug("Adding Peer {} , {}@{}".format(pid, host, port))
            
        # Peer dictionary structure defined here
        self.add_store(
            pid, dictionary=Peer(pid, key, host, port).dict
        )
        
        # init stream buffer
        self.peer_stream_buffer[pid] = []
        
        # Add peer to swarm graph
        if constants.NETWORKX_AVAILABLE:
            self.add_swarm_graph_node(pid)

    def delete_peer(self, pid):
        "Remove unauth peer."
        
        Logger.warn("Peer [{}] left swarm.".format(pid))
        # remove peer connection 
        del self.peer_connections[pid]

        return self.delete_store(pid)

    def get_peer(self, pid):
        "Get peer from db."
        
        return self.get_store(pid)

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
            self.set_store_item(pid, "PEER_STATUS", status)
        else:
            raise Exception(
                "Invalid Peer Connection Status, must be True or False."
            )

    def list_peer_ids(self):
        "Returns a list of all peer IDs present in swarm."
        
        try:
            return self.keys()

        except AttributeError:
            return []
        
    def list_peers(self):
        "Returns a list of all the peers."

        peerlist = []

        for k in self.keys():

            # Get peer attributes
            p_info = self.get_store(k)
            
            # Concat if key is bigger than 4 chars
            if len(p_info["PEER_KEY"]) >=4:
                peer_key = p_info["PEER_KEY"][0:3] + "XXXX"
            else:
                peer_key = p_info["PEER_KEY"]
                 
            # Append as tuples (peer id, peer host, peer port, peer status)
            peerlist.append(
                (p_info["PEER_ID"],
                 peer_key,
                 p_info["PEER_IP"],
                 p_info["PEER_PORT"],
                 p_info["PEER_STATUS"]))

        return peerlist
    
    def list_peer_id_colors(self):
        "Returns a list of all the peers."

        rcclist = [self.my_msg_rcc]

        for sid in self.keys():
            # Get peer color attributes
            rcclist.append(
                self.get_store_item(sid, "PEER_COLOR")
            )

        return rcclist
    
    def peer_table(self):
        "Display all peers"
        
        table= self.storage_table()
        
        if table:
            return table
        else:
            return "No peers in swarm."

    def peer_host(self, pid):
        "Returns a peer's IPv4 address."

        return self.get_store_item(pid, "PEER_IP")

    ## Need to simplify mapping TODO
    def get_peerid_from_ip(self, peer_ip, peer_port=constants.PEER_PORT):
        "Get a peerid from stored IP addresses. Assumes 1to1 relation."

        for (pid, _, ip, port, _) in self.list_peers():
            if ip == peer_ip and port == peer_port:
                return pid

        return None  # Add relevent catch

    def get_peer_connection_status(self, pid):
        "Get the peer connection status."

        return self.get_store_item(pid, "PEER_STATUS")

    def get_peer_connection(self, pid):
        "Get the peer connection."

        return self.peer_connections[pid]

    def get_peer_key(self, pid):
        "Get the peers key."

        return self.get_store_item(pid, "PEER_KEY")
        
    def get_peerid_color(self, pid):
        "Return peer's color code."
        
        pid_rcc = self.get_store_item(pid, "PEER_COLOR")
               
        if pid_rcc:
            return pid_rcc
        else:
            return self.my_msg_rcc
        
    def is_peer(self, pid):
        "Check if peer got added successfully."
        
        return self.in_store(pid)       
    
    def add_stream_buffer(self, pid, stream_id):
        "Add pending streams to peer stream buffer"
        
        self.peer_stream_buffer[pid].append(stream_id)
        
    def get_stream_buffer(self, pid):
        "Return stream buffer"
        
        return self.peer_stream_buffer[pid]
    
    # Swarm Graphing functions
    if constants.NETWORKX_AVAILABLE:
        def add_swarm_graph_node(self, pid):
            "Add peer node to swarm graph."
    
            self.swarm_graph.add_edge(self.my_peerid, pid)
            
        def plot_swarm_graph(self):
            "Visualize the swarm"
            
            # Plot circular graph
            nx.draw_circular(self.swarm_graph)

            # Show graph plot
            plt.show()   
            
            return True         

if __name__ == '__main__':
    sm = SwarmManager(1000, "key")
    sm.add_peer(123, "k1", 'localhost', 8000)
    sm.add_peer(234, "k2", 'localhost', 8001)
    sm.add_peer(345, "k3", 'localhost', 8002)
    sm.add_peer(456, "k4", 'localhost', 8003)
    print sm.list_peers()
