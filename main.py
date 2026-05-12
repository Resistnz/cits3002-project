import sys
import config
from devices import Host, Router, PhysicalLink

def setup_network():
    """
    Initializes Host A, Router R1, and Host B.
    Wires them together using PhysicalLink instances.
    """
    host_a = Host("Host A", config.HOST_A_IP, config.HOST_A_MAC, config.HOST_A_ROUTING_TABLE, config.HOST_A_MAC_TABLE)
    host_b = Host("Host B", config.HOST_B_IP, config.HOST_B_MAC, config.HOST_B_ROUTING_TABLE, config.HOST_B_MAC_TABLE)
    
    router_config = {
        1: {'ip': config.ROUTER_R1_IF1_IP, 'mac': config.ROUTER_R1_IF1_MAC},
        2: {'ip': config.ROUTER_R1_IF2_IP, 'mac': config.ROUTER_R1_IF2_MAC}
    }
    router = Router("Router R1", router_config, config.ROUTER_R1_ROUTING_TABLE, config.ROUTER_R1_MAC_TABLE)

    link_a_to_r1 = PhysicalLink(host_a, 1, router, 1)
    link_r1_to_b = PhysicalLink(router, 2, host_b, 1)

    return host_a, router, host_b

def main():
    """
    Parses command-line arguments for message size.
    Initializes the network topology.
    Triggers Host A to send the payload to Host B.
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <message_size_in_bytes>")
        sys.exit(1)
        
    try:
        message_size = int(sys.argv[1])
    except ValueError:
        print("Error: Message size must be an integer.")
        sys.exit(1)

    host_a, router, host_b = setup_network()
    
    # Trigger the simulation
    host_a.send_message("A" * message_size, config.HOST_B_IP)

if __name__ == "__main__":
    main()