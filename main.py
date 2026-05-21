import sys
import config
from devices import Host, Router, Wire

def setup_network():
    """Initialise our hosts and wire them together"""
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
    """Take command line input, set up the network and send a message"""
    if len(sys.argv) != 2:
        print("Usage: python main.py <message_size_in_bytes>")
        sys.exit(1)
        
    try:
        message_size = int(sys.argv[1])
    except ValueError:
        print("Error: Message size must be an integer.")
        sys.exit(1)

    host_a, router, host_b = setup_network()
    
    # Make it so
    host_a.send_message(b"A" * message_size, config.HOST_B_IP)

if __name__ == "__main__":
    main()