from pickletools import read_decimalnl_long
from Record import *
from helper import *
import ipaddress
import struct



class RecordMX(Record):
    def __init__(self, name, typ, ttl, rdlength, authorative,  rcv , offsetToData ):
        super().__init__(name, typ, ttl, rdlength, authorative, rcv ,offsetToData)
        self.pref , self.exc, self.offsetToData = self.processMX()

        



    def processMX(self):
        pref = struct.Struct("!H").unpack_from(self.rcv, self.offsetToData)[0]
        offset = self.offsetToData + 2
        exc, offset = labelToString(self.rcv , offset)
        exc = b'.'.join(self.overwrite(exc)).decode()
        return pref , exc , offset

    def overwrite(self,exc):
        if  isinstance(exc, list) == False:
            return [exc]
        
        data = []
        for i in exc:
            if isinstance(i, list) == True:  
                data += self.overwrite(i)
            elif isinstance(i,int) == False:
                data.append(i)
            else:
                pass

        return data
