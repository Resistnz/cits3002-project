import sys
import config
from devices import Host, Router, PhysicalLink

def setup_network():
    """
    Initializes Host A, Router R1, and Host B.
    Wires them together using PhysicalLink instances.
    """
    host_a = Host(config.HOST_A_IP, config.HOST_A_MAC, config.HOST_A_ROUTING_TABLE)
    host_b = Host(config.HOST_B_IP, config.HOST_B_MAC, config.HOST_B_ROUTING_TABLE)
    router = Router(config.ROUTER_R1_IF1_IP, config.ROUTER_R1_IF1_MAC, config.ROUTER_R1_IF2_IP, config.ROUTER_R1_IF2_MAC, config.ROUTER_R1_ROUTING_TABLE)

    link_a_to_r1 = PhysicalLink(host_a, router)
    link_r1_to_b = PhysicalLink(router, host_b)

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
    host_a.generate_traffic(message_size, config.HOST_B_IP)

if __name__ == "__main__":
    main()