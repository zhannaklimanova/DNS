DNS Client in python (network tool)

Need python3

Usage : python dnsClient [-t timeout] [-r max-retries] [-p port] [-mx|-ns] @server 

(e.g python3 dnsClient.py @8.8.8.8 mcgill.ca)

Parameters:<br /> 
•timeout(optional) gives how long to wait, inseconds, before retransmitting an
unanswered query. Default value: 5.<br /> 
• max-retries(optional) is the maximum number of times to retransmit an
unanswered query before giving up. Default value: 3.<br /> 
• port(optional) is theUDP port number ofthe DNS server. Default value: 53.<br /> 
• -mx or -ns flags (optional) indicate whether to send a MX (mail server) or NS (name server)
query.At most one of these can be given, and if neither is given then the client should send a
type A (IP address) query.<br /> 
• server (required) is the IPv4 address of the DNS server, in a.b.c.d.format<br /> 
• name (required) is the domain name to query for.<br /> 

To run 3 different queries:
python3 dnsClient.py @8.8.8.8 -ns azuki.com
python3 dnsClient.py @8.8.8.8 -mx azuki.com
python3 dnsClient.py @8.8.8.8 azuki.com
