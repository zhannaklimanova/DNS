class Header:
    def __init__(self, ID, QR, Opcode, AA, TC, RD, RA, Z, RCode, QDCount, ANCount, NSCount, ARCount):
        # ID
        self.ID = ID

        # Flags
        self.QR = QR 
        self.Opcode = Opcode
        self.AA = AA
        self.TC = TC
        self.RD = RD
        self.RA = RA
        self.Z = Z
        self.RCode = RCode

        # QDCOUNT
        self.QDCount = QDCount

        # ANCOUNT
        self.ANCount = ANCount

        # NSCOUNT
        self.NSCount = NSCount

        # ARCOUNT
        self.ARCount = ARCount

    def get_ID(self):
        return self.ID

    def get_flags(self):
        flags = self.QR + self.Opcode + self.AA + self.TC + self.RD + self.RA + self.Z + self.RCode
        return int(flags, 2)

    def get_QDCount(self):
        return int(self.QDCount)

    def get_ANCount(self):
        return int(self.ANCount)

    def get_NSCount(self):
        return int(self.NSCount)

    def get_ARCount(self):
        return int(self.ARCount)
    



    def get_QR(self):
        return int(self.QR)

    def get_OpCode(self):
        return int(self.Opcode)

    def get_AA(self):
        return int(self.AA, 2)

    def get_TC(self):
        return int(self.TC, 2)

    def get_RD(self):
        return int(self.RD, 2)

    def get_RA(self):
        return int(self.RA, 2)

    def get_Z(self):
        return int(self.Z, 2)

    def get_RCode(self):
        return int(self.RCode, 2)