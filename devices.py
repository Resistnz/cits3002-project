from protocols import DataLinkLayer, NetworkLayer, TransportLayer

class Wire:
    """Simulate a wire between two interfaces on two devices"""
    def __init__(self, device1, iface1: int, device2, iface2: int):
        self.device1 = device1
        self.iface1 = iface1
        self.device2 = device2
        self.iface2 = iface2
        
        # Automatically connect the devices to this link
        self.device1.connect(iface1, self)
        self.device2.connect(iface2, self)

    # Deliver the frame to the device on the other end
    def transmit(self, frame, source_device):
        if source_device == self.device1.name:
            self.device2.l2.receive_from_physical(frame, self.iface2)
        elif source_device == self.device2.name:
            self.device1.l2.receive_from_physical(frame, self.iface1)

class Node:
    def __init__(self, name: str):
        self.name = name
        self.interfaces = {} # Hardware interfaces connected to Wires

    # Attach a physical link to an interface
    def connect(self, interface_id: int, link: Wire):
        self.interfaces[interface_id] = link

class Host(Node):
    """Device that contains Layers 2, 3, and 4"""
    def __init__(self, name: str, ip: str, mac: str, routing_table: dict, mac_table: dict = None):
        super().__init__(name)
        self.ip = ip
        self.mac = mac
        self.ips = {1: ip}
        self.macs = {1: mac}
        
        # Instantiate and link layers
        self.l2 = DataLinkLayer(name, self.interfaces, self.macs, mac_table)
        self.l3 = NetworkLayer(name, self.ips, routing_table, self.l2)
        self.l4 = TransportLayer(name, self.l3)
        
        # Wire the layers together internally
        self.l2.network_layer = self.l3
        self.l3.transport_layer = self.l4

    def send_message(self, message: str, dest_ip: str):
        """Simulate the Application Layer sending data. WE don't actually do anything here"""

        self.l4.receive_from_application(message, self.ip, dest_ip)

class Router(Node):
    """Device containing only Layers 2 and 3"""
    def __init__(self, name: str, interfaces_config: dict, routing_table: dict, mac_table: dict = None):
        super().__init__(name)
        self.ips = {iface: conf['ip'] for iface, conf in interfaces_config.items()}
        self.macs = {iface: conf['mac'] for iface, conf in interfaces_config.items()}

        # Routers do not have a Transport Layer
        self.l2 = DataLinkLayer(name, self.interfaces, self.macs, mac_table)
        self.l3 = NetworkLayer(name, self.ips, routing_table, self.l2)
        
        self.l2.network_layer = self.l3