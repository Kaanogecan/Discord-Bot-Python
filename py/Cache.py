import datetime
class Cache():
    def __init__(self, value, cacheTimeOut):
        self._value = value
        self.UpdatedTime = datetime.datetime.now()
        self.CacheTimeOut = cacheTimeOut
    def CalculateTimeDiff(self):
        difference = (datetime.datetime.now() - self.UpdatedTime).total_seconds()
        return (difference > self.CacheTimeOut)

    def SetValue(self,value):
        self._value = value
        self.UpdatedTime = datetime.datetime.now()

    def GetValue(self):
        if self.CalculateTimeDiff():
            self._value = ""
        return self._value

    