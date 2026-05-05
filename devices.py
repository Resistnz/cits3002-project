from protocols import DataLinkLayer, NetworkLayer, TransportLayer

class PhysicalLink:
    """Simulates a wire between two specific interfaces on two devices."""
    def __init__(self, device1, iface1: int, device2, iface2: int):
        self.device1 = device1
        self.iface1 = iface1
        self.device2 = device2
        self.iface2 = iface2

    def transmit(self, frame, source_device):
        """Delivers the frame to the opposite device's Data Link layer."""
        pass

class Node:
    """Base class for any networked device."""
    def __init__(self, name: str):
        self.name = name
        self.interfaces = {} # Hardware interfaces connected to PhysicalLinks

    def connect(self, interface_id: int, link: PhysicalLink):
        """Attaches a physical link to an interface."""
        pass

class Host(Node):
    """End-device containing Layers 2, 3, and 4."""
    def __init__(self, name: str, ip: str, mac: str, routing_table: dict):
        super().__init__(name)
        self.ip = ip
        self.mac = mac
        
        # Instantiate and link layers
        self.l2 = DataLinkLayer(name, self.interfaces)
        self.l3 = NetworkLayer(name, routing_table, self.l2)
        self.l4 = TransportLayer(name, self.l3)
        
        # Wire the layers together internally
        self.l2.network_layer = self.l3
        self.l3.transport_layer = self.l4

    def generate_traffic(self, message_size_bytes: int, dest_ip: str):
        """Simulates the Application Layer sending data."""
        pass

class Router(Node):
    """Intermediate device containing only Layers 2 and 3."""
    def __init__(self, name: str, routing_table: dict):
        super().__init__(name)
        
        # Routers do not have a Transport Layer
        self.l2 = DataLinkLayer(name, self.interfaces)
        self.l3 = NetworkLayer(name, routing_table, self.l2)
        
        self.l2.network_layer = self.l3