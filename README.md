# cits3002-project
24214277 - Tobias Camille
24245674 - Kamlesh Senthilkumar

Zero generative AI was used in this project or this structure explanation.

# Structure
Our simulation uses `Hosts` and `Routers` that communicate via functions in the Layer classes (`TransportLayer`, `NetworkLayer` and `DataLinkLayer` as defined in `protocol.py`).

In each layer, a function of the form `send_to_XXX_layer()` and `recieve_from_XXX_layer()` handles the traversal of packets between layers. Within each layer, the packet is encapsulated, headers added, and then sent to the next layer. 

Each `Host` has its own `Layer` instance, and are connected to other hosts with a `Wire` instance.

## The Journey of a Message
More specific information can be found in the function header comments and code.

`Host.send_message(message, dest_ip)` gets called to start the simulation, which just calls `recieve_from_application()` in the `TransportLayer`. From here, the message is repeatedly encapsulated (`L4Segment`, then `L3Packet`, then `L2Frame`) until it reaches the `DataLinkLayer`.

### Between Devices
Once a frame is ready to be sent to another device, the layer uses its `self.interfaces` list (analogous to physical ethernet ports) to find the attached `Wire` class. This `Wire` class simulates a physical connection between 2 devices, which passes the frame the the `DataLinkLayer` on the recieving device.

### Routers
If the recieving device is a `Router`, the frame gets sent up to the `NetworkLayer`, but no further. We test if the destination IP address is the same as the current device IP, and if not, it must be a `Router`. The `Router` then sends it back down to the `DataLinkLayer` and forwards it out along the other interface (and then down a `Wire`).

### Acknowledgment
One a message reaches the Host `TransportLayer`, an ACK frame must be sent (assuming our checksum is ok). We send back an `ACK` segment, with a sequence number following `rdt2.2`. Once Host A recieves the `ACK` frame, it can go ahead and continue sending segments. If Host A does not recieve the `ACK` (e.g. the checksum fails and the packet gets dropped), Host B will continue sending `ACK` messages (stop-and-wait).


## File Structure
Our layer and frame/segment/packet classes all live in `protocol.py`, while the device classes are in `devices.py`.

Our main file `main.py` handles starting the simulation, where it loads in our network config from `config.py`.