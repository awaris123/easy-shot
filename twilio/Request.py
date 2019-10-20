class Request(object):


    ''' Class to represent user request '''

    def __init__(self, cat = "", ts="", num=""):
        self.category = cat
        self.timeStamp = ts
        self.number = num

    def isSameUsr(self, address):
        return address.number == self.number

    def inTimeRange(self, address):
        return address.timeStamp == self.timeStamp

