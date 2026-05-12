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

    def log(self, message: str):
        print(f"{self.host_name} Layer 4: {message}")

    def receive_from_application(self, data: str, dest_ip: str):
        """Chunks data into 500-byte max segments, applies rdt2.2 transmission."""

        # TODO: Data chunking

        self.log(f"Received from Application Layer. Data size={len(data)}")

        segment = L4Segment(src_port=12345, dst_port=80, seq_num=self.seq_num, is_ack=False, data=data)
        self.send_segment(segment, dest_ip)

    def send_segment(self, segment: L4Segment, dest_ip: str):
        """Computes checksum, encapsulates, and sends to Layer 3."""

        segment.checksum = self._compute_checksum(segment.data)

        self.log(f"Checksum computed")
        self.log(f"Segment created by adding transport layer header (DATA,seq={segment.seq_num}) (encapsulation)")
        self.log(f"Segment sent to Network Layer")

        self.network_layer.receive_from_transport(segment, self.host_name, dest_ip)

    def receive_from_network(self, segment: L4Segment, src_ip: str):
        """Verifies checksum, processes ACK or DATA, and sends to App or retransmits."""

        if not self._verify_checksum(segment):
            # Checksum failed, ignore segment
            return
        
        # TODO: ACK

        print(segment.data)

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

    def log(self, message: str):
        print(f"{self.device_name} Layer 3: {message}")

    def receive_from_transport(self, segment: L4Segment, src_ip: str, dst_ip: str):
        """Encapsulates segment into L3Packet and performs routing."""

        self.log(f"Segment received from Transport Layer. SRC_IP={src_ip}, DST_IP={dst_ip}, TTL=100")

        packet = L3Packet(src_ip=src_ip, dst_ip=dst_ip, payload=segment)
        self._route_packet(packet)

        pass

    def receive_from_datalink(self, packet: L3Packet, interface: int):
        """Decrements TTL, drops if 0. Checks if local delivery or needs forwarding."""

        packet.ttl -= 1
        if packet.ttl <= 0:
            return
        
        if packet.dst_ip == self.device_name:
            self.transport_layer.receive_from_network(packet.payload, packet.src_ip)
        else:
            self._route_packet(packet)

        pass

    def _route_packet(self, packet: L3Packet):
        """Looks up dst_ip in routing_table, determines next-hop and interface."""

        dest_ip = packet.dst_ip

        self.log("Destination IP read: " + dest_ip)

        next_hop_ip, interface = self.routing_table[dest_ip]

        self.log("Routing table lookup performed")
        self.log("Next-hop IP determined: " + next_hop_ip)

        self.log("Packet forwarded to Data Link Layer")
        self.datalink_layer.receive_from_network(packet, next_hop_ip, interface)

        pass

class DataLinkLayer:
    """Layer 2: Handles MAC learning, framing, and physical forwarding."""
    def __init__(self, device_name: str, interfaces: dict):
        self.device_name = device_name
        self.interfaces = interfaces # Map of interface_id -> physical_link
        self.mac_table = {}          # Map of Next_Hop_IP -> MAC (Simplified ARP)
        self.network_layer = None

    def log(self, message: str):
        print(f"{self.device_name} Layer 2: {message}")

    def receive_from_network(self, packet: L3Packet, next_hop_ip: str, interface: int):
        """Looks up destination MAC, creates frame, and transmits on interface."""

        self.log(f"Packet recieved from Network Layer")

        dst_mac = self.mac_table[next_hop_ip]

        self.log(f"Destination MAC lookup for next-hop IP ({next_hop_ip}) → {dst_mac}")

        frame = L2Frame(src_mac=self.interfaces[interface].device1.mac, dst_mac=dst_mac, payload=packet)

        self.log(f"Frame Created: SRC_MAC={frame.src_mac}, DST_MAC={frame.dst_mac}")

        self.interfaces[interface].transmit(frame, self.device_name)

        pass

    def receive_from_physical(self, frame: L2Frame, interface: int):
        """Learns source MAC, decapsulates, and delivers to Network Layer."""

        self.mac_table[frame.src_mac] = frame.src_mac
        self.network_layer.receive_from_datalink(frame.payload, interface)

        pass