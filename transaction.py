class grantRevokeTransaction(object):
    def __init__(self, typ = None, patAddr = None, serAddr = None, serReqAddr = None, sig = None,):
        self.typeT = typ
        self.patientAddress = patAddr
        self.serviceProAddress = serAddr
        self.serviceReqAddress = serReqAddr
        self.signature = sig


class recordTransaction(object):
    def __init__(self, patAddr = None, serAddr = None, hash = None, oldHash = None, sig = None,):
        self.patientAddress = patAddr
        self.serviceProAddress = serAddr
        self.hash = hash
        self.oldHash = oldHash
        self.signature = sig


class keyInclusionTransaction(object):
    def __init__(self, patAddr = None, publicKey = None, sig = None,):
        self.patientAddress = patAddr
        self.publicKey = publicKey
        self.signature = sig


if __name__ == '__main__':
    ojb = grantRevokeTransaction()




