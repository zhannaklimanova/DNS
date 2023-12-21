from pickletools import read_decimalnl_long
from Record import *
import ipaddress
import struct



class RecordA(Record):
    def __init__(self, name, typ, ttl, rdlength, authorative,  rcv , offsetToData ):
        super().__init__(name, typ, ttl, rdlength, authorative, rcv ,offsetToData)
        self.rdata  = self.processA()[0]

        



    def processA(self):
        rdata = struct.Struct("!I").unpack_from(self.rcv, self.offsetToData)[0]
        offset = self.offsetToData + self.rdlength
        ip = str(ipaddress.IPv4Address(rdata))
        

        return ip , offset

    def newOffset(self):
        return self.processA()[1]
