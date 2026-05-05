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

# Routing Tables: Maps Destination Subnet/IP -> (Next Hop IP, Outgoing Interface)
# Example format: { "10.0.2.0/24": ("10.0.2.20", 2) }
HOST_A_ROUTING_TABLE = {}
HOST_B_ROUTING_TABLE = {}
ROUTER_R1_ROUTING_TABLE = {}