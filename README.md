# CITS3002, Mini Internet Protocol Stack Simulator (Python)
## Contributors
24214277 - Tobias Camille
24245674 - Kamlesh Senthilkumar

## File Structure
```text
24214277-24245674/
├── main.py
├── protocol.py
├── devices.py
├── config.py
└── README.md
```
- Note: A documentation pdf (24214277-24245674.pdf) detailing design choices and justifications is located outside the code repository.

### Project organisation
- main.py is the entry point for the simulator. 
- protocol.py contains protocol layer and protocol data unit implementations. 
- devices.py defines the network topology components: Hosts, Routers, and Wire connection link.
- config.py stores project-specified network configuration values.

Our layer and frame/segment/packet classes all live in `protocol.py`, while the device classes are in `devices.py`. Our main file `main.py` handles starting the simulation, where it loads in our network config from `config.py`.

## Running the Program
Run the simulator using the following in your terminal/commandline prompt:
- Ensure you are in the correct directory 24214277-24245674.
```bash
python3 main.py <message_size_in_bytes>
```

For example:

```bash
python3 main.py 100
```
This simulates the network with a 100-byte application message from Host A to Host B via Router R1.

# Structure
Our simulation uses `Hosts` and `Routers` that communicate via functions in the Layer classes (`TransportLayer`, `NetworkLayer` and `DataLinkLayer` as defined in `protocol.py`).

In each layer, a function of the form `send_to_XXX_layer()` and `receive_from_XXX_layer()` handles the traversal of packets between layers. Within each layer, the packet is encapsulated, headers added, and then sent to the next layer. 

Each `Host` has its own layer instances and is connected to the other host with a `Wire` instance.

## The Journey of a Message
More specific information can be found in the function header comments and code.

`Host.send_message(message, dest_ip)` gets called to start the simulation, which just calls `receive_from_application()` in the `TransportLayer`. From here, the message is repeatedly encapsulated (`L4Segment`, then `L3Packet`, then `L2Frame`) until it reaches the `DataLinkLayer`.

### Between Devices
Once a frame is ready to be sent to another device, the layer uses its `self.interfaces` list (analogous to physical ethernet ports) to find the attached `Wire` class. This `Wire` class simulates a physical connection between two device interfaces and forwards Layer 2 frames between them.

### Routers
If the receiving device is a `Router`, the frame gets sent up to the `NetworkLayer`, but no further. The router checks if the destination IP address is the same as the current device IP address. If it is not the same, it must be a `Router` device, not one of the host devices. The `Router` then sends packet back down to the `DataLinkLayer` and forwards it out along the other interface (and then down a `Wire`).

### Acknowledgment
Once a message reaches the Host `TransportLayer`, an ACK frame must be sent (assuming our checksum is OK). We send back an `ACK` segment, with a sequence number following `rdt2.2`. Once Host A receives the `ACK` frame, it can go ahead and continue sending segments. If Host A does not receive the `ACK` (e.g. the checksum fails and the packet gets dropped), Host B will continue sending `ACK` messages (stop-and-wait).


Zero generative AI was used in this project or this structure explanation.