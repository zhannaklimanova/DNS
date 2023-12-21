from email.base64mime import header_length
import socket
from xmlrpc.client import boolean
from helper import *
from QueryFlag import *
from Header import *
from Question import *
from Record import *
from RecordA import *
from RecordMX import *
from RecordNS import *
from QueryFlag import *
import struct
import time
import random



class Client: 
    headerLength = 0
    questionLength = 0
    qNameLength = 0
    numOfRetries = 0
    def __init__(self, timeout, maxRetries, port, queryFlagVal, serverIP, hostName):
        self.timeout = timeout
        self.maxRetries = maxRetries
        self.port = port
        self.queryFlagVal = queryFlagVal
        self.serverIP = serverIP
        self.hostName = hostName

    # https://docs.python.org/3/library/stdtypes.html#int.to_bytes
    def create_packet(self):
        header = Header(random.getrandbits(16), "0", "0000", "0", "0", "1", "0", "000", "0000", "1", "0", "0", "0")
        question = Question(self.hostName, self.queryFlagVal, "1")

        # Header 
        dnsPacket = random.getrandbits(16).to_bytes(2, byteorder='big') # ID
        dnsPacket += header.get_flags().to_bytes(2, byteorder='big') # Flags: QR| Opcode |AA|TC|RD|RA| Z | RCODE
        dnsPacket += header.get_QDCount().to_bytes(2, byteorder='big')  # QDCOUNT
        dnsPacket += header.get_ANCount().to_bytes(2, byteorder='big')  # ANCOUNT
        dnsPacket += header.get_NSCount().to_bytes(2, byteorder='big')  # NSCOUNT
        dnsPacket += header.get_ARCount().to_bytes(2, byteorder='big')  # ARCOUNT
        self.headerLength = len(dnsPacket)

        # Question
        dnsPacket = question.get_QName(dnsPacket) # QNAME
        self.qNameLength = len(dnsPacket) - self.headerLength
        dnsPacket += question.get_QType().to_bytes(2, byteorder='big') # QTYPE
        dnsPacket += question.get_QClass().to_bytes(2, byteorder='big')  # QCLASS

        self.questionLength = len(dnsPacket) - self.headerLength

        

        
        return dnsPacket


    def convert_flags(self, binaryFlags):
        binaryFlags = binaryFlags[2:] # strip string of 0b chars
        flags = {
            "QR": "",
            "OpCode": "",
            "AA": "",
            "TC": "",
            "RD": "",
            "RA": "",
            "Z": "", 
            "RCode": ""
        }
        flags["QR"] = binaryFlags[0]
        flags["OpCode"] = binaryFlags[1:5]
        flags["AA"] = binaryFlags[5]
        flags["TC"] = binaryFlags[6]
        flags["RD"] = binaryFlags[7]
        flags["RA"] = binaryFlags[8]
        flags["Z"] = binaryFlags[9:12]
        flags["RCode"] = binaryFlags[13:16]

        return flags  

    
    def test_RCode_error(self, RCode):
        if RCode == 1: 
            return "Format error: the name server was unable to interpret the query."
        elif RCode == 2: 
            return "Server failure: the name server was unable to process this query due to a problem with the name server."
        elif RCode == 3: 
            return "NOTFOUND"
        elif RCode == 4: 
            return "Not implemented: the name server does not support the requested kind of query."
        elif RCode == 5: 
            return "Refused: the name server refuses to perform the requested operation for policy reasons."      
        else: 
            return ""

    def test_RA_error(self, RA):
        if RA == 0: 
            return "The server provided does not support recursive queries." 
        else: 
            return ""

    def test_TC_truncation(self, TC):
        if TC == 1: 
            return "The message was truncated because it had a length greater than that permitted by the transmission channel." 
        else: 
            return ""

    def decode_received_DNS_packet(self, receivedBuffer): 
        halfWordOffset = 2
        wordOffset = 4

        # print("Received Packet")
        # print(receivedBuffer, len(receivedBuffer))

        # self.receivedHeader["id"] = struct.unpack_from("!H",self.receivedBuffer, 0)[0]
        # self.receivedHeader["arr"] = struct.unpack_from("!H", self.receivedBuffer, 2)[0]
        # print("binary", bin(struct.unpack_from("!H", receivedBuffer, 2)[0]))
        # print("binarylength", type(bin(self.receivedHeader["arr"])))
        # print("FLAGS", self.convert_flags( bin(self.receivedHeader["arr"])))
        receivedHeaderFlags = self.convert_flags(bin(struct.unpack_from("!H", receivedBuffer, 2)[0]))
        # self.receivedHeader["qdcount"] = struct.unpack_from("!H", self.receivedBuffer, 4)[0]
        # self.receivedHeader["ancount"] = struct.unpack_from("!H", self.receivedBuffer, 6)[0]
        # self.receivedHeader["nscount"] = struct.unpack_from("!H", self.receivedBuffer, 8)[0]
        # self.receivedHeader["arcount"] = struct.unpack_from("!H", self.receivedBuffer, 10)[0]

        decodedHeader = Header(
            struct.unpack_from("!H",receivedBuffer, 0)[0], # ID
            receivedHeaderFlags["QR"], # QR
            receivedHeaderFlags["OpCode"], # Opcode
            receivedHeaderFlags["AA"], # AA: meaningful in response packets and indicates whether 1 or 0 the server is an authority 
            receivedHeaderFlags["TC"], # RC
            receivedHeaderFlags["RD"], # RD
            receivedHeaderFlags["RA"], # RA
            receivedHeaderFlags["Z"],  # Z
            receivedHeaderFlags["RCode"], # RCODE
            struct.unpack_from("!H", receivedBuffer, 4)[0], # QDCOUNT
            struct.unpack_from("!H", receivedBuffer, 6)[0], # ANCOUNT
            struct.unpack_from("!H", receivedBuffer, 8)[0], # NSCOUNT
            struct.unpack_from("!H", receivedBuffer, 10)[0] # ARCOUNT
        )

        # print(decodedHeader.get_ID(), decodedHeader.get_QR(), decodedHeader.get_OpCode(), decodedHeader.get_AA(), decodedHeader.get_TC(), decodedHeader.get_RD(), decodedHeader.get_RA(), decodedHeader.get_Z(), decodedHeader.get_RCode(), decodedHeader.get_QDCount(), decodedHeader.get_ANCount(), decodedHeader.get_NSCount(), decodedHeader.get_ARCount())
        # self.isAuthoritative = is_authoritative(decodedHeader.get_AA())
        # print("isAuthoritative", self.isAuthoritative)

        if self.test_RCode_error(decodedHeader.get_RCode()) != "":
            print(self.test_RCode_error(decodedHeader.get_RCode()))
            exit(1)
    



        if (self.test_RA_error(decodedHeader.get_RA)) != "":
            print("RA Error Report: ", self.test_RA_error(decodedHeader.get_RA))
      


        if self.test_TC_truncation(decodedHeader.get_TC) != "":
            print("TA Truncation Report: ", self.test_TC_truncation(decodedHeader.get_TC))
       

        # TODO later
        # receivedHostName = ""
        # for byteCounter in range(self.lengthHeader, (self.lengthHeader + self.lengthQName)):
        #     # byte = chr(struct.unpack_from("!B", self.receivedBuffer, byteCounter)[0])
        #     # if byte == "":
        #     #     receivedHostName += "."
        #     # receivedHostName += struct.unpack_from("!B", self.receivedBuffer, byteCounter)[0]
        #     print(struct.unpack_from("!B", self.receivedBuffer, byteCounter)[0])

        # print(receivedHostName)
        
        # self.receivedQuestion["qname"] = self.hostName
        # self.receivedQuestion["qtype"] = struct.unpack_from("!H", self.receivedBuffer, self.lengthHeader + self.lengthQName)[0]
        # self.receivedQuestion["qclass"] = struct.unpack_from("!H", self.receivedBuffer, self.lengthHeader + self.lengthQName + self.lengthQType)[0]

        # self.receivedAnswer["name"] = struct.unpack_from("!H", self.receivedBuffer, self.lengthQuery)[0] # pointer to hostName in header section 
        # self.receivedAnswer["type"] = struct.unpack_from("!H", self.receivedBuffer, self.lengthQuery + halfWordOffset)[0]
        # self.receivedAnswer["class"] = struct.unpack_from("!H", self.receivedBuffer, self.lengthQuery + halfWordOffset + halfWordOffset)[0]
        # self.receivedAnswer["ttl"] = struct.unpack_from("!H", self.receivedBuffer, self.lengthQuery + halfWordOffset + halfWordOffset + wordOffset)[0]
        # self.receivedAnswer["rdlength"] = struct.unpack_from("!H", self.receivedBuffer, self.lengthQuery + halfWordOffset + halfWordOffset + wordOffset + halfWordOffset)[0]
        # self.handle_RData_field(self.queryFlagVal, self.receivedBuffer[self.lengthQuery + halfWordOffset + halfWordOffset + wordOffset + halfWordOffset + halfWordOffset: self.lengthReceivedPacket])

        # print(self.receivedHeader["id"], self.receivedHeader["arr"], self.receivedHeader["qdcount"], self.receivedHeader["ancount"], self.receivedHeader["nscount"], self.receivedHeader["arcount"], "____", self.receivedQuestion["qname"], self.receivedQuestion["qtype"], self.receivedQuestion["qclass"])
        # print(self.receivedAnswer["name"], self.receivedAnswer["type"], self.receivedAnswer["class"], self.receivedAnswer["ttl"], self.receivedAnswer["rdlength"])


    
    def sendRequest(self):
        # Initiating DNS client socket
        try:
            dnsClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET: underlying network is IPv4. SOCK_DGRAM: UDP socket. 
            dnsClientSocket.settimeout(int(self.timeout))
            
            # Send request to DNS server
            dnsClientSocket.sendto(self.create_packet(), (self.serverIP.replace("@", ""), int(self.port))) # b/c IP address is used, DNS lookup must be done manually (fix this)



            # Receive DNS server response
            receivedBuffer, receivedIPAddress = dnsClientSocket.recvfrom(512) # safest UDP packet size is 512 bytes while avoiding packet fragmentation. If larger, TCP must be used
            
            self.decode_received_DNS_packet(receivedBuffer)
            
            id = struct.unpack_from("!H",receivedBuffer, 0)[0]
            arr = struct.unpack_from("!H" , receivedBuffer , 2)[0]
            ancount = struct.unpack_from("!H" , receivedBuffer , 6)[0]
            nscount = struct.unpack_from("!H" , receivedBuffer , 8)[0]
            arccount = struct.unpack_from("!H" , receivedBuffer , 10)[0]
            
            AA = (arr & 0x0400) != 0
            offset = self.headerLength + self.questionLength 
            answersData, offset = self.get_Ans_Add_Auth(receivedBuffer ,offset , ancount, AA)
            authorativeData , offset = self.get_Ans_Add_Auth(receivedBuffer ,offset , nscount, AA)
            additionalData, offset = self.get_Ans_Add_Auth(receivedBuffer ,offset , arccount, AA)

            anyRecord = False

            if(ancount >0):
                print(f"***Answer Section ({len(answersData)} records)***")
                anyRecord = True
                for i in answersData:
                    if (isinstance(i,RecordA)):
                        print(f"IP\t{i.rdata}\t{i.ttl}\t{i.authorative}")

                    elif (isinstance(i,RecordNS)):
                        print(f"NS\t{i.rdata}\t{i.ttl}\t{i.authorative}")


                    elif(isinstance(i, RecordMX)):
                        print(f"MX\t{i.exc}\t{i.pref}\t{i.ttl}\t\n{i.authorative}")
            
            if(nscount >0):
                print(f"***Authoritative Section ({len(authorativeData)} records)***")
                anyRecord = True
                for i in authorativeData:
                    if (isinstance(i,RecordA)):
                        print(f"IP\t{i.rdata}\t{i.ttl}\t{i.authorative}")

                    elif (isinstance(i,RecordNS)):
                        print(f"NS\t{i.rdata}\t{i.ttl}\t{i.authorative}")

                    elif(isinstance(i, RecordMX)):
                        print(f"MX\t{i.exc}\t{i.pref}\t{i.ttl}\t\n{i.authorative}")

            
            if(arccount >0):
                print(f"***Additional Section ({len(additionalData)} records)***")
                anyRecord = True
                for i in additionalData:
                    if (isinstance(i,RecordA)):
                        print(f"IP\t{i.rdata}\t{i.ttl}\t{i.authorative}")

                    elif (isinstance(i,RecordNS)):
                        print(f"NS\t{i.rdata}\t{i.ttl}\t{i.authorative}")
                    
                    elif(isinstance(i, RecordMX)):
                        print(f"MX\t{i.exc}\t{i.pref}\t{i.ttl}\t\n{i.authorative}")


                 
                    
            if (anyRecord == False):
                self.maxRetries
                print('Unknown QueryFlag')



            dnsClientSocket.close()

            return receivedBuffer
        except socket.timeout as e:
            if(self.numOfRetries>self.maxRetries):
                print("ERROR: Maximum number of retries" , self.maxRetries, "exceeded")
            else:
                self.numOfRetries = self.numOfRetries +1

        except Exception as e:
            print("ERROR: ", e)



      



     
    def get_Ans_Add_Auth(self, rcv, offset, counter , AA):
    #let's get the Client.label first
        data = []
        for _ in range(counter):
            nameSec, offset = labelToString(rcv,offset)
            typeSec   = struct.Struct("!2H").unpack_from(rcv,offset)[0]
            offset = offset + 4
            ttlSec  = struct.Struct("!I").unpack_from(rcv, offset)[0]
            offset = offset + 4
            rdlength = struct.Struct("!H").unpack_from(rcv, offset)[0]
            offset = offset + 2
            record = None
          
            if typeSec == QueryFlag.A:
                record = RecordA(nameSec, typeSec, ttlSec, rdlength ,AA, rcv , offset)  
                offset = record.newOffset()
                data.append(record)
                 
                
            elif typeSec == QueryFlag.MX:
                record = RecordMX(nameSec, typeSec, ttlSec, rdlength ,AA, rcv , offset)
                offset = record.offsetToData
                data.append(record)

            elif typeSec == QueryFlag.NS:
                record = RecordNS(nameSec, typeSec, ttlSec, rdlength, AA, rcv, offset)
                offset= record.offsetToData
                data.append(record)

            else:
                offset = offset + rdlength
                pass


           

            
        return data , offset




        

    

    



# TODO change the print statements to proper formatting with padding specifications
  

