class sendRequestForAccess(object):
    def __init__(self, from_ = None, to_ = None, hospitalID = None, diseaseID = None):
        self.from_ = from_
        self.to_ = to_
        self.hospitalID = hospitalID
        self.diseaseID = diseaseID


class sendRecord(object):
    def __init__(self, patAddr = None, hospitalID = None, hash = None, docLink = None, diseaseID = None,):
        self.from_ = hospitalID
        self.to_ = patAddr
        self.diseaseID = diseaseID
        self.hash = hash
        self.docLink = docLink
        self.premmissions = [hospitalID]


class grantAccessToRecord(object):
    def __init__(self, from_ = None, to_ = None, hospitalID = None, diseaseID = None):
        self.from_ = from_
        self.to_ = to_
        self.hospitalID = hospitalID
        self.diseaseID = diseaseID


if __name__ == '__main__':
    ojb = grantRevokeTransaction()
