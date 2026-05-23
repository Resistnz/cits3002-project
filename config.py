"""
config.py

This script defines network parameters and project-specified configuration values used during network simulation.
- IP addresses
- MAC addresses
- Routing tables
- Transport layer configuration values
"""
# Transport Layer Configuration:
# Defined maximum payload size for a Layer 4 (Transport layer) segment
MAX_SEGMENT_DATA_SIZE = 500 

# Device Address Configuration:
# Defined IP and MAC addresses used by hosts and routers
HOST_A_IP = "10.0.1.10"
HOST_A_MAC = "AA:AA:AA:AA:AA:AA"

HOST_B_IP = "10.0.2.20"
HOST_B_MAC = "DD:DD:DD:DD:DD:DD"

ROUTER_R1_IF1_IP = "10.0.1.1"
ROUTER_R1_IF1_MAC = "BB:BB:BB:BB:BB:BB"

ROUTER_R1_IF2_IP = "10.0.2.1"
ROUTER_R1_IF2_MAC = "CC:CC:CC:CC:CC:CC"

# Routing Tables:
# Destination Network -> (Next Hop IP, Outgoing Interface)
# If next-hop IP address is None, the destination network is directly connected. Router interface and packets forwarded directly
HOST_A_ROUTING_TABLE = {"10.0.2.20": ("10.0.1.1", 1)}
HOST_B_ROUTING_TABLE = {"10.0.1.10": ("10.0.2.1", 1)}
ROUTER_R1_ROUTING_TABLE = {"10.0.1.10": (None, 1), "10.0.2.20": (None, 2)}

# MAC Address Tables:
# Maps next-hop IP address to destination MAC addresses. Utilised by data-link layer for frame destination determination
HOST_A_MAC_TABLE = {"10.0.1.1": ROUTER_R1_IF1_MAC}
HOST_B_MAC_TABLE = {"10.0.2.1": ROUTER_R1_IF2_MAC}
ROUTER_R1_MAC_TABLE = {HOST_A_IP: HOST_A_MAC, HOST_B_IP: HOST_B_MAC}