import datetime
class Time:
        def __init__(self, hour = 0 , minute = 0):
                self.hour = hour
                self.minute = minute
        def __eq__(self, other):
                if((self.hour == other.hour) and (self.minute == self.hour)):
                        return True
                else:
                        return False
        def __gt__(self, other):
                if ( self.hour == other.hour ):
                        if( self.minute > other.minute):
                                return True
                        else:
                                return False
                else:
                        if(self.hour > other.hour):
                                return True
                        else:
                                return False
        def __lt__(self,other):
                if ( self.hour == other.hour ):
                        if( self.minute < other.minute):
                                return True
                        else:
                                return False
                else:
                        if(self.hour < other.hour):
                                return True
                        else:
                                return False
        def __le__(sekf, other):
                if( (slef<other) or (self == other) ):
                        return True
                else:
                        return False
        def __ge__(self,other):
                if ( (self>other) or (self == other) ):
                        return True
                else:
                        return False
        def __str__(self):
                return str(self.hour)+":"+str(self.minute)
        def load(self,mystr):
                mylist = mystr.split(':')
                self.hour = int(mylist[0])
                self.minute = int(mylist[1])
        def set_now(self):
                currentDT = datetime.datetime.now()
                self.hour = currentDT.hour
                self.minute = currentDT.minute

