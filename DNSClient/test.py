import struct
import random
from Header import Header
from Client import *


# packet = struct.pack("B",1) # ID
# packet = struct.pack(">H", 256) # Flags
# packet += struct.pack("B", 0)  # End of String

# print(packet)
# stuff = (256).to_bytes(2, byteorder='big')
# print((256).to_bytes(2, byteorder='big'))

# print(stuff + packet)

dnsHeader = Header(random.getrandbits(16), "1", "0011", "1", "1", "1", "0", "011", "0101", "1", "1", "0", "1")

dnsClient = Client(7, 6, 5, 4, 5, 5)

# print(dnsClient.create_packet(), type(dnsClient.create_packet()))


# t = "@8.8.8.8"
# t = t.replace("@", "")
# print(t)


# print(packet)

split_url = "www.mcgill.ca"
for part in split_url:
            # parts = part.encode('utf-8')
            # packet += (len(part)).to_bytes(1, byteorder='big') #struct.pack("B", len(part))
            for byte in part:
               print(byte)