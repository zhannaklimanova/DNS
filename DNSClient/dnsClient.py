from ctypes import sizeof
import time
from helper import *
from Client import Client

def main(): 
    inputArgs = argument_parser()
    validate_server_IP(inputArgs.server)


    # Setting constructor arguments
    timeout = inputArgs.timeout
    maxRetries = inputArgs.maxRetries
    port = inputArgs.port

    if inputArgs.mx:
        queryFlagVal = determine_query("mx")
        query = "MX"
    elif inputArgs.ns:
        queryFlagVal = determine_query("ns")
        query = "NS"
    else:
        queryFlagVal = determine_query("A")
        query = "A"

    serverIP = inputArgs.server
    hostName = inputArgs.name


    print("DNS Client sending request for ",hostName)
    print("Server: ",serverIP[1:])
    print("Request type:" ,query)
    dnsClient = Client(timeout, maxRetries, port, queryFlagVal, serverIP, hostName)

    start = time.time()
    dnsClient.sendRequest()
    end = time.time()
    responseTime = (end-start)
    print("Response received after" , round(responseTime,3),"seconds (",dnsClient.numOfRetries,"retries)" )
    




if __name__ == "__main__":
    main()

