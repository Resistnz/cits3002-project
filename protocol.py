"""
protocol.py
This script implements protocol data unit (PDU) definitions of each layer and protocol stack layer functions:

Protocol data units:
- L4Segment: Transport-layer segment
- L3Packet: Network-layer packet
- L2Frame: Data Link-layer frame

Class definitions and methods of each layer of protocol stack.
Protocol layers:
- TransportLayer: segmentation, checksum verification, and rdt2.2 logic
- NetworkLayer: packet routing, forwarding, and TTL handling
- DataLinkLayer: framing, MAC learning, and local frame delivery
"""
class L4Segment:
    """Transport Layer (UDP-like) Segment."""
    def __init__(self, src_port: int, dst_port: int, seq_num: int, is_ack: bool, data: bytes, checksum: int = 0):
        """Initialise transport-layer header fields and data payload"""
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num = seq_num
        self.is_ack = is_ack
        self.data = data # Data payload
        self.checksum = checksum
        self.length = len(self.data) + 8 # Size of transport-layer header

class L3Packet:
    """Network Layer (IP-like) Packet."""
    def __init__(self, src_ip: str, dst_ip: str, payload: L4Segment, ttl: int = 100):
        """Initialise network layer header fields and encapsulate data segment from transport layer"""
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ttl = ttl
        self.payload = payload
        self.protocol = 17
        self.total_length = 20 + payload.length

class L2Frame:
    """Data Link Layer (Ethernet-like) Frame"""
    def __init__(self, src_mac: str, dst_mac: str, payload: L3Packet):
        """Initialise data-link layer header fields and encapsulate data packet from network layer"""
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.payload = payload
        self.type = 0x0800 

class TransportLayer:
    """Implementation of Transport layer. This class is responsible for:
    - segmentation of application layer data
    - calculation and verification of checksums
    - rdt2.2 acknowledgements
    - perform re-transmissions
    - data delivery between applications and network layer
    """
    def __init__(self, host_name: str, network_layer):
        """Initialise transport layer variables for sending and receiving end system"""
        self.host_name = host_name
        self.network_layer = network_layer

        # Sender state
        self.seq_num = 0 # rdt2.2 state (0 or 1)
        self.waiting_for_ack = False
        self.last_ack_received = None
        self.current_segment = None

        # Receiver state
        self.expected_seq_num = 0

    def log(self, message: str):
        """Function for printing string-formatted Layer 4 log message"""
        print(f"{self.host_name}: Layer 4: {message}")

    def receive_from_application(self, data: bytes, src_ip: str, dest_ip: str):
        """Get application data, segment it into chunks of max 500 bytes, 
        and transmit to the network layer using rdt2.2 stop-and-wait"""

        self.log(f"Data received from Application Layer. Data size={len(data)}")

        # Split data into 500-byte chunks
        for i in range(0, len(data), 500):
            chunk = data[i:i + 500]

            # Create DATA segment
            segment = L4Segment(src_port=12345, dst_port=80, seq_num=self.seq_num, is_ack=False, data=chunk) 

            # Save current segment in case we need to retransmit it
            self.current_segment = segment
            
            # Stop-and-wait send loop
            ack_received = False
            while not ack_received:
                self.waiting_for_ack = True
                self.last_ack_received = None

                self.send_segment(segment, src_ip, dest_ip)

                # Simplified implementation of ACK handling by nested method calls
                if self.last_ack_received == segment.seq_num:
                    ack_received = True
                    self.waiting_for_ack = False

                    # Alternate the rdt2.2 sequence number between 0 and 1.
                    if self.seq_num == 0:
                        self.seq_num = 1
                    else:
                        self.seq_num = 0

                else:
                    self.log(f"Incorrect ACK received. Retransmitting segment seq={segment.seq_num}")

    def send_segment(self, segment: L4Segment, src_ip: str, dest_ip: str):
        """Compute checksum and forward segment to the network Layer"""

        # First compute checksum before transmission
        segment.checksum = self.compute_checksum(segment.data)
        
        # Only log "Checksum computed" for DATA segments to match expected log
        if not segment.is_ack:
            self.log("Checksum computed")

        #Host A, moving down is DATA. HostB will be ACK. 
        # This is used for logging output
        segment_type = "ACK" if segment.is_ack else "DATA" 

        encap_str = " (encapsulation)" if not segment.is_ack else ""
        self.log(f"Segment created by adding transport layer header ({segment_type}, seq={segment.seq_num}){encap_str}")
        self.log("Segment sent to Network Layer")

        self.network_layer.receive_from_transport(segment, src_ip, dest_ip)

    def receive_from_network(self, segment: L4Segment, src_ip: str, dst_ip: str):
        """Calculate checksum for incoming transport layer data segment.
        Verify checksums, perform acknowledgements and detect duplicate transmission.
        Valid data is sent to application layer.
        """

        print()
        self.log("Segment received from Network Layer")

        # Verify the checksum first (for both DATA and ACK segments)
        if not self.verify_checksum(segment):
            self.log("Checksum failed!!! Segment discarded") 

            if segment.is_ack:
                # In simple synchronous simulation, ignore corrupted ACKs
                return

            # Re-send ACK for the last correctly received packet
            if self.expected_seq_num == 0:
                previous_ack = 1
            else:
                previous_ack = 0
            
            ack_segment = L4Segment(src_port=12345, dst_port=80, seq_num=previous_ack, is_ack=True, data=b"")
            self.send_segment(ack_segment, dst_ip, src_ip)
            return

        self.log("Checksum verified")

        # ACK Processing (Sender Side)
        if segment.is_ack:
            self.log(f"ACK received: seq={segment.seq_num}")
            self.last_ack_received = segment.seq_num
            return

        # DATA Processing (Receiver Side)
        # Correct expected data segment received
        if segment.seq_num == self.expected_seq_num:

            self.log(f"DATA segment delivered to Application Layer. " f"Data size={len(segment.data)}")

            # Send ACK for correctly received segment
            ack_segment = L4Segment(src_port=12345, dst_port=80, seq_num=segment.seq_num, is_ack=True, data=b"")
            self.send_segment(ack_segment, dst_ip, src_ip)

            # Switch expected sequence number for next packet
            if self.expected_seq_num == 0:
                self.expected_seq_num = 1
            else:
                self.expected_seq_num = 0

        # Incorrect, Duplicate data segment received
        else:
            self.log(f"Duplicate DATA segment received. " f"Expected seq={self.expected_seq_num}, " f"received seq={segment.seq_num}")

            # Send ACK again for the last valid packet
            if self.expected_seq_num == 0:
                previous_ack = 1
            else:
                previous_ack = 0

            ack_segment = L4Segment(src_port=12345, dst_port=80, seq_num=previous_ack, is_ack=True, data=b"")
            self.send_segment(ack_segment, dst_ip, src_ip)

    def compute_checksum(self, data: bytes) -> int:
        """Calculate standard Internet Checksum of data. Inspired from Week 8 lecture"""
        total = 0

        # Handle padding for an odd number of bytes
        if len(data) % 2 != 0:
            data += b'\x00'

        # Sum 16-bit chunks
        for i in range(0, len(data), 2):
            # Just bitshift and add 2 chars to get 16 bit word
            word = (data[i] << 8) + data[i + 1]
            total += word
            
        # Do the end carry-over bits
        while (total >> 16) > 0:
            total = (total & 0xFFFF) + (total >> 16)
            
        # 1's complement of the result
        return ~total & 0xFFFF

    def verify_checksum(self, segment: L4Segment) -> bool:
        """Recalculate the checksum and compare checksum for data integrity verification"""
        computed_checksum = self.compute_checksum(segment.data)

        return computed_checksum == segment.checksum

class NetworkLayer:
    """Implementation of Network layer. This class is responsible for:
    - Packet encapsulation
    - Routing decisions
    - Packet forwarding
    - TTL handling
    - Delivery between the transport and data-link layers
    """
    def __init__(self, device_name: str, ips: dict, routing_table: dict, datalink_layer):
        """Initialise network-layer addressing and routing information"""
        self.device_name = device_name
        self.ips = ips
        self.routing_table = routing_table
        self.datalink_layer = datalink_layer
        self.transport_layer = None # Transport layer only present devices which are hosts

    def log(self, message: str):
        print(f"{self.device_name}: Layer 3: {message}")

    def receive_from_transport(self, segment: L4Segment, src_ip: str, dst_ip: str):
        """Encapsulate segment into network packet and perform routing"""

        print()

        self.log(f"Segment received from Transport Layer: SRC_IP={src_ip}, DST_IP={dst_ip}, TTL=100")
        self.log(f"Destination IP read: {dst_ip}")

        packet = L3Packet(src_ip=src_ip, dst_ip=dst_ip, payload=segment)
        self._route_packet(packet)

    def receive_from_datalink(self, packet: L3Packet, interface: int):
        """Decrement TTL, and drop if 0. Check if is local delivery or needs forwarding"""

        print()
        
        self.log(f"Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        self.log(f"Destination IP read: {packet.dst_ip}")

        # If this packet is for us, send it up to transport layer
        if packet.dst_ip in self.ips.values():
            self.log(f"Packet identified as local delivery")
            self.log(f"Segment delivered to Transport Layer")
            self.transport_layer.receive_from_network(packet.payload, packet.src_ip, packet.dst_ip)
        # Forward packet to the next hop
        else:
            packet.ttl -= 1

            self.log(f"TTL decremented: {packet.ttl + 1} -> {packet.ttl}")

            if packet.ttl <= 0:
                self.log("Packet dropped due to TTL expiry")
                return

            self._route_packet(packet)

    def _route_packet(self, packet: L3Packet):
        """Perform lookup in routing-table and forward the data packet to the data-link layer."""

        dest_ip = packet.dst_ip

        next_hop_ip, interface = self.routing_table[dest_ip]

        # If next_hop_ip is None, the destination is directly connected (e.g. from the router)
        if next_hop_ip is None:
            next_hop_ip = dest_ip

        self.log("Routing table lookup performed")
        self.log("Next-hop IP determined: " + next_hop_ip)

        if "Router" in self.device_name:
            self.log(f"Outgoing interface selected (Interface {interface})")
        else:
            self.log("Outgoing interface selected")

        self.log("Packet forwarded to Data Link Layer")
        self.datalink_layer.receive_from_network(packet, next_hop_ip, interface)

class DataLinkLayer:
    """Implementation of Data-link layer. This class is responsible for:
    - Creation of data frame
    - MAC address learning
    - Local frame forwarding
    - Delivery between the network layer and physical links
    """
    def __init__(self, device_name: str, interfaces: dict, macs: dict, initial_mac_table: dict = None):
        """Initialise interface mappings and MAC address tables"""
        self.device_name = device_name
        self.interfaces = interfaces # interface_id -> physical_link
        self.macs = macs                 # interface_id -> mac
        self.mac_table = initial_mac_table if initial_mac_table else {} # Maps next-hop IPs to MAC addresses 
        self.network_layer = None

    def log(self, message: str):
        print(f"{self.device_name}: Layer 2: {message}")

    def receive_from_network(self, packet: L3Packet, next_hop_ip: str, interface: int):
        """Encapsulate packet into data frame, look up destination MAC address, create data frame, and transmit it across interface"""

        print()
        self.log(f"Packet received from Network Layer")

        dst_mac = self.mac_table[next_hop_ip]

        self.log(f"Destination MAC lookup for next-hop IP ({next_hop_ip}) -> {dst_mac}")

        frame = L2Frame(src_mac=self.macs[interface], dst_mac=dst_mac, payload=packet)

        self.log(f"Frame created: SRC_MAC={frame.src_mac}, DST_MAC={frame.dst_mac}")
        
        if "Router" in self.device_name:
            self.log(f"Frame forwarded on Interface {interface}")
        else:
            self.log(f"Frame sent")

        self.interfaces[interface].transmit(frame, self.device_name)

    def receive_from_physical(self, frame: L2Frame, interface: int):
        """Process an incoming data frame from the connection link. 
        Learn source MAC address, decapsulate the data frame, and delivers packet to network layer"""

        print()
        if "Router" in self.device_name:
            self.log(f"Frame received on Interface {interface}")
        else:
            self.log(f"Frame received")

        self.mac_table[frame.payload.src_ip] = frame.src_mac

        if "Router" in self.device_name:
            self.log(f"Source MAC learned: {frame.src_mac} on Interface {interface}")
        else:
            self.log(f"Source MAC learned: {frame.src_mac}")
            
        self.log(f"Packet delivered to Network Layer")

        self.network_layer.receive_from_datalink(frame.payload, interface)