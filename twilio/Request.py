class Request(object):


    ''' Class to represent user request '''

    def __init__(self, cat = "", ts="", num=1, s_loc=""):
        self.category = cat
        self.timeStamp = ts
        self.number = num
        # self.hash = hash(1.0 / num)
        self.s_loc = ""

    def isSameUsr(self, address):
        return address.number == self.number

    def inTimeRange(self, address):
        return address.timeStamp == self.timeStamp
