"""
config.py
Defines fixed network parameters, IP/MAC addresses, and routing tables.
"""

# Maximum payload size for a Layer 4 segment
MAX_SEGMENT_DATA_SIZE = 500

# Device Addresses
HOST_A_IP = "10.0.1.10"
HOST_A_MAC = "AA:AA:AA:AA:AA:AA"

HOST_B_IP = "10.0.2.20"
HOST_B_MAC = "DD:DD:DD:DD:DD:DD"

ROUTER_R1_IF1_IP = "10.0.1.1"
ROUTER_R1_IF1_MAC = "BB:BB:BB:BB:BB:BB"

ROUTER_R1_IF2_IP = "10.0.2.1"
ROUTER_R1_IF2_MAC = "CC:CC:CC:CC:CC:CC"

# Destination Network -> (Next Hop IP, Outgoing Interface)
# If Next Hop IP is None, it is a directly connected network
HOST_A_ROUTING_TABLE = {"10.0.2.20": ("10.0.1.1", 1)}
HOST_B_ROUTING_TABLE = {"10.0.1.10": ("10.0.2.1", 1)}
ROUTER_R1_ROUTING_TABLE = {"10.0.1.10": (None, 1), "10.0.2.20": (None, 2)}

# Simplified ARP Tables: Maps Next Hop IP -> MAC Address
HOST_A_MAC_TABLE = {"10.0.1.1": ROUTER_R1_IF1_MAC}
HOST_B_MAC_TABLE = {"10.0.2.1": ROUTER_R1_IF2_MAC}
ROUTER_R1_MAC_TABLE = {HOST_A_IP: HOST_A_MAC, HOST_B_IP: HOST_B_MAC}