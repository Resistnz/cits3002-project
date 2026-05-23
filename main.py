"""
main.py

This script is the main entry file used to initialise computer network and function call. Responsible for:
- Initialising components in computer network topology
- Creating instances of hosts, routers and connection links
- Processing command line input to send message
- Calling an end-to-end transmission of message
"""
import sys
import config
from devices import Host, Router, Wire

def setup_network():
    """Initialise components in our network topology. Initialise: 
    - Hosts A and B
    - Router R1
    - Wire connection between devices in network"""
    host_a = Host("Host A", config.HOST_A_IP, config.HOST_A_MAC, config.HOST_A_ROUTING_TABLE, config.HOST_A_MAC_TABLE)
    host_b = Host("Host B", config.HOST_B_IP, config.HOST_B_MAC, config.HOST_B_ROUTING_TABLE, config.HOST_B_MAC_TABLE)
    
    router_config = {
        1: {'ip': config.ROUTER_R1_IF1_IP, 'mac': config.ROUTER_R1_IF1_MAC},
        2: {'ip': config.ROUTER_R1_IF2_IP, 'mac': config.ROUTER_R1_IF2_MAC}
    }
    router = Router("Router R1", router_config, config.ROUTER_R1_ROUTING_TABLE, config.ROUTER_R1_MAC_TABLE)

    a_to_r1 = Wire(host_a, 1, router, 1)
    r1_to_b = Wire(router, 2, host_b, 1)

    return host_a, router, host_b

def main():
    """Read the command line input, set up the network by calling setup_network() function above
    and transmit a message from Host A to Host B"""
    # Input sanitisation, user must message size argument
    if len(sys.argv) != 2:
        print("Usage: python main.py <message_size_in_bytes>")
        sys.exit(1)

    # Input message size is extracted from command line    
    try:
        message_size = int(sys.argv[1])
    except ValueError:
        print("Error: Message size must be an integer.")
        sys.exit(1)

    host_a, router, host_b = setup_network()
    
    # Begin an end-to-end message transmission
    # Here we generate a 'dummy' application message of the specified size
    host_a.send_message(b"A" * message_size, config.HOST_B_IP)

if __name__ == "__main__":
    main()