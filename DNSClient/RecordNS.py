from concurrent.futures import process
from pickletools import read_decimalnl_long
from Record import *
from helper import *
import ipaddress
import struct



class RecordNS(Record):
    def __init__(self, name, typ, ttl, rdlength, authorative,  rcv , offsetToData):
        super().__init__(name, typ, ttl, rdlength, authorative, rcv ,offsetToData)
        self.rdata = self.processNS()[0]

        



    def processNS(self):
        rdata, offset = labelToString(self.rcv, self.offsetToData)
        rdata = b'.'.join(self.overwrite(rdata)).decode()
        self.offsetToData = offset
        return rdata , offset
    


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


        