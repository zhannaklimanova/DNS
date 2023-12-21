import argparse
import struct
from QueryFlag import *

# resource used https://docs.python.org/3/library/argparse.html
def argument_parser():
    # Optional arguments 
    parser = argparse.ArgumentParser(description='Process the input arguments for the DNS client program.')
    parser.add_argument('-t', dest='timeout', default=5, help='gives how long to wait in seconds, before transmitting an unaswered query. Default value:5')
    parser.add_argument('-r', dest='maxRetries', default=3, help='the maximum number of times to retransmit an unanswered query before giving up. Default value: 3')
    parser.add_argument('-p', dest='port',  default=53, help='the UDP port number of the DNS server. Default value: 53')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-mx', dest='mx', action='store_true', default=False, help='send a mail server query')
    group.add_argument('-ns', dest='ns', action='store_true', default=False, help='send a name server query')

    # Positional arguments - required
    parser.add_argument(action="store", type=str, dest="server", help="the IPv4 address of the DNS server, in a.b.c.d.format")
    parser.add_argument(action="store", type=str, dest="name", help="the domain name to query for")

    # parser.print_help() # for testing

    return parser.parse_args()


def validate_server_IP(serverIP):
    ip = serverIP[1:len(serverIP)]

    if serverIP.find('@') == 0:
        ipv4 = validate_ip_address(ip)

        if not ipv4:
            print("Server IPV4 address {} is invalid".format(serverIP))
            print("Correct Usage for server: @a.b.c.d where a, b, c, and d are integers in the range [0, 255].")
            print("Example: @8.8.8.8")
            exit(1)
    else:  
        print("Missing @ before IPV4 server.")
        exit(1)



def validate_ip_address(address):
    parts = address.split(".")

    if len(parts) != 4:
        return False

    for part in parts:
        if not isinstance(int(part), int):
            return False

        if int(part) < 0 or int(part) > 255:
            return False
    return True        

def determine_query(queryType):
    if queryType == "mx":
        return QueryFlag.MX
    elif queryType == "ns":
        return QueryFlag.NS
    elif queryType == "A":
        return QueryFlag.A




def labelToString(rcv, offset):
    arr = []
    looping = True
    while looping:
        l = struct.unpack_from("!B", rcv, offset)[0]
        if (l & 0xC0 ) == 0xC0:
            ptr = struct.unpack_from("!H", rcv,offset)[0] & 0x3FFF
            offset = offset + 2
            l1 = list(arr)
            l2 = list(labelToString(rcv,ptr))
            temp = []
            temp = [*l1 , *l2] 
            Looping = False
            return temp, offset


        offset = offset + 1
        if l == 0:
            Looping = False
            return arr,offset
    
        arr.append(*struct.unpack_from("!%ds" % l, rcv, offset))
        offset += l
    if(not Looping):
        print("ERROR")