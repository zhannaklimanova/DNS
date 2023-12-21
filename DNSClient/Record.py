
class Record:
    

    def __init__(self, name ,typ , ttl, rdlength, authorative, rcv, offsetToData):
        self.name = name
        self.typ = typ
        self.ttl = ttl
        self.rdlength = rdlength
        self.authorative = authorative
        self.rcv = rcv
        self.offsetToData = offsetToData


