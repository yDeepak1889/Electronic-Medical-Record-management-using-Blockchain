class sendRequestForAccess(object):
    def __init__(self, from_ = None, to_ = None, hospitalID = None, diseaseID = None):
        self.from_ = from_
        self.to_ = to_
        self.hospitalID = hospitalID
        self.diseaseID = diseaseID
    
    def getType():
        return 0;


class submitRecord(object):
    def __init__(self, patAddr = None, hospitalID = None, hash = None, docLink = None, diseaseID = None,):
        self.from_ = hospitalID
        self.to_ = patAddr
        self.diseaseID = diseaseID
        self.hash = hash
        self.docLink = docLink
        self.premmissions = [hospitalID]

    def getType():
        return 1;


class grantAccessToRecord(object):
    def __init__(self, from_ = None, to_ = None, hospitalID = None, diseaseID = None):
        self.from_ = from_
        self.to_ = to_
        self.hospitalID = hospitalID
        self.diseaseID = diseaseID

    def getType():
        return 2;

