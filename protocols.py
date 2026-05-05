class DataLinkLayer():
    def __init__(self):
        self.destination_mac : str = None
        self.source_mac : str = None
        self.type : int = None
        self.payload : NetworkLayer = None

class NetworkLayer():
    def __init__(self):
        self.destination_ip : str = None
        self.source_ip : str = None
        self.ttl : int = None
        self.protocol : int = None
        self.total_length : int = None
        self.payload : TransportLayer = None

class TransportLayer():
    def __init__(self):
        self.source_port : int = None
        self.destination_port : int = None
        self.length : int = None
        self.checksum : int = None
        self.type : int = None
        self.sequence_number : int = None
        self.data : str = None