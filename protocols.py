# --- Header Definitions ---

class L4Segment:
    """Represents a Transport Layer (UDP-like) Segment."""
    def __init__(self, src_port: int, dst_port: int, seq_num: int, is_ack: bool, data: str, checksum: int = 0):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num = seq_num
        self.is_ack = is_ack
        self.data = data
        self.checksum = checksum
        self.length = len(self.data) + 8 # Example header size

class L3Packet:
    """Represents a Network Layer (IP-like) Packet."""
    def __init__(self, src_ip: str, dst_ip: str, payload: L4Segment, ttl: int = 100):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ttl = ttl
        self.payload = payload

class L2Frame:
    """Represents a Data Link Layer (Ethernet-like) Frame."""
    def __init__(self, src_mac: str, dst_mac: str, payload: L3Packet):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.payload = payload

# --- Layer Implementations ---

class TransportLayer:
    """Layer 4: Handles port delivery, segmentation, checksums, and rdt2.2."""
    def __init__(self, host_name: str, network_layer):
        self.host_name = host_name
        self.network_layer = network_layer
        self.seq_num = 0  # rdt2.2 state (0 or 1)
        self.expected_seq_num = 0

    def receive_from_application(self, data: str, dest_ip: str):
        """Chunks data into 500-byte max segments, applies rdt2.2 transmission."""

        segment = L4Segment(src_port=12345, dst_port=80, seq_num=self.seq_num, is_ack=False, data=data)
        self.send_segment(segment, dest_ip)

        pass

    def send_segment(self, segment: L4Segment, dest_ip: str):
        """Computes checksum, encapsulates, and sends to Layer 3."""

        segment.checksum = self._compute_checksum(segment.data)
        self.network_layer.receive_from_transport(segment, self.host_name, dest_ip)

        pass

    def receive_from_network(self, segment: L4Segment, src_ip: str):
        """Verifies checksum, processes ACK or DATA, and sends to App or retransmits."""
        pass

    def _compute_checksum(self, data: str) -> int:
        """Calculates a simple checksum for error detection."""
        pass

    def _verify_checksum(self, segment: L4Segment) -> bool:
        """Validates the segment against its checksum."""
        pass

class NetworkLayer:
    """Layer 3: Handles IP routing, TTL, and logical forwarding."""
    def __init__(self, device_name: str, routing_table: dict, datalink_layer):
        self.device_name = device_name
        self.routing_table = routing_table
        self.datalink_layer = datalink_layer
        self.transport_layer = None # Linked if device is a Host

    def receive_from_transport(self, segment: L4Segment, src_ip: str, dst_ip: str):
        """Encapsulates segment into L3Packet and performs routing."""

        packet = L3Packet(src_ip=src_ip, dst_ip=dst_ip, payload=segment)
        self._route_packet(packet)

        pass

    def receive_from_datalink(self, packet: L3Packet, interface: int):
        """Decrements TTL, drops if 0. Checks if local delivery or needs forwarding."""
        pass

    def _route_packet(self, packet: L3Packet):
        """Looks up dst_ip in routing_table, determines next-hop and interface."""

        dest_ip = packet.dst_ip
        if dest_ip in self.routing_table:
            next_hop_ip, interface = self.routing_table[dest_ip]
            self.datalink_layer.receive_from_network(packet, next_hop_ip, interface)

        pass

class DataLinkLayer:
    """Layer 2: Handles MAC learning, framing, and physical forwarding."""
    def __init__(self, device_name: str, interfaces: dict):
        self.device_name = device_name
        self.interfaces = interfaces # Map of interface_id -> physical_link
        self.mac_table = {}          # Map of Next_Hop_IP -> MAC (Simplified ARP)
        self.network_layer = None

    def receive_from_network(self, packet: L3Packet, next_hop_ip: str, interface: int):
        """Looks up destination MAC, creates frame, and transmits on interface."""

        if next_hop_ip in self.mac_table:
            dst_mac = self.mac_table[next_hop_ip]

            frame = L2Frame(src_mac=self.interfaces[interface].device1.mac, dst_mac=dst_mac, payload=packet)
            self.interfaces[interface].transmit(frame, self.device_name)

        pass

    def receive_from_physical(self, frame: L2Frame, interface: int):
        """Learns source MAC, decapsulates, and delivers to Network Layer."""

        self.mac_table[frame.src_mac] = frame.src_mac
        self.network_layer.receive_from_datalink(frame.payload, interface)

        pass

    def _forward_frame(self, frame: L2Frame, interface: int):
        """Pushes the frame onto the simulated physical link."""
        pass