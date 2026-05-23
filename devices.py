"""
devices.py

This script implements the classes for hosts, routers and connection link abstraction used in network simulation.

- Wire: simulates a physical connection link between device interfaces
- Node: base class for devices connected in network 
- Hosts: end systems which contain protocol stack layers 2, 3 and 4
- Routers: route data packets from source to destination device. Contain protocol stack layers 2 and 3
"""
from protocol import DataLinkLayer, NetworkLayer, TransportLayer

class Wire:
    """Simulate a wire connection link between two interfaces on two devices"""
    def __init__(self, device1, iface1: int, device2, iface2: int):
        """Initialise a bidirectional connection link between two device interfaces"""
        self.device1 = device1
        self.iface1 = iface1
        self.device2 = device2
        self.iface2 = iface2
        
        # Automatically connect the devices with this link
        self.device1.connect(iface1, self)
        self.device2.connect(iface2, self)

    def transmit(self, frame, source_device):
        """Transmit a data-link layer frame from across connection link from source to destination end system"""
        if source_device == self.device1.name:
            self.device2.l2.receive_from_physical(frame, self.iface2)
        elif source_device == self.device2.name:
            self.device1.l2.receive_from_physical(frame, self.iface1)

class Node:
    """A class which represents base model for devices connected to the network"""
    def __init__(self, name: str):
        """Initialise a device with name and interface table"""
        self.name = name
        self.interfaces = {} # Hardware interfaces connected to Wires

    def connect(self, interface_id: int, link: Wire):
        """Attach a Wire object (a connection link) to a device interface"""
        self.interfaces[interface_id] = link

class Host(Node):
    """Class which represents an end system connected to network. 
    Host contains all protocol stack layers: 
    - Data-link layer
    - Network layer
    - Transport layer
    """
    def __init__(self, name: str, ip: str, mac: str, routing_table: dict, mac_table: dict = None):
        """Initialise a host device"""
        super().__init__(name)
        self.ip = ip
        self.mac = mac
        self.ips = {1: ip}
        self.macs = {1: mac}
        
        # Instantiate instances of protocol layer used by host
        self.l2 = DataLinkLayer(name, self.interfaces, self.macs, mac_table)
        self.l3 = NetworkLayer(name, self.ips, routing_table, self.l2)
        self.l4 = TransportLayer(name, self.l3)
        
        # Connect protocl layers together (this connection is between adjacent layers of protocol stack)
        self.l2.network_layer = self.l3
        self.l3.transport_layer = self.l4

    def send_message(self, message: str, dest_ip: str):
        """Simulate the Application Layer sending data. 
        Included for completeness, but functionality for this projec begins in Transport layer.
        """

        self.l4.receive_from_application(message, self.ip, dest_ip)

class Router(Node):
    """Router contains data-link and network layers."""
    def __init__(self, name: str, interfaces_config: dict, routing_table: dict, mac_table: dict = None):
        """Initialise the interfaces of router and instances of protocl layers"""
        super().__init__(name)
        self.ips = {iface: conf['ip'] for iface, conf in interfaces_config.items()}
        self.macs = {iface: conf['mac'] for iface, conf in interfaces_config.items()}

        # Routers do not have a Transport Layer. They are only used to forward data packets.
        self.l2 = DataLinkLayer(name, self.interfaces, self.macs, mac_table)
        self.l3 = NetworkLayer(name, self.ips, routing_table, self.l2)
        
        self.l2.network_layer = self.l3