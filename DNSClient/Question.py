class Question:
    def __init__(self, QName, QType, QClass):
        # QNAME
        self.QName = QName

        # QTYPE
        self.QType = QType 

        # QCLASS
        self.QClass = QClass
    

    def get_QName(self, packetHeader):
        for part in self.QName.split("."):
            packetHeader += (len(part)).to_bytes(1, byteorder='big') 
            for byte in part:
                packetHeader += (byte.encode('utf-8')) 
        packetHeader += (0).to_bytes(1, byteorder='big')  # End of String

        return packetHeader 

    def get_QType(self):
        return self.QType

    def get_QClass(self):
        return int(self.QClass)

    

    
