#!/usr/bin/python
from SessionStatus import SessionStatus

class SessionStatistics:
    def __init__(self):
        self.statistics = {SessionStatus.INITIAL    : 0, 
                           SessionStatus.CONNECTING : 0,
                           SessionStatus.SETUP      : 0,
                           SessionStatus.RUNNING    : 0, 
                           SessionStatus.STOPPED    : 0,
                           SessionStatus.NETWORKERROR : 0,
                           SessionStatus.EXECPTION  : 0,
                           SessionStatus.REMOVED    : 0,
                           SessionStatus.PAUSE      : 0}

    def __setitem__(self, key, value):
        self.statistics[key] = value

    def __getitem__(self, key):
        return self.statistics[key]
    
    def __iadd__(self, other):
        for key in self.statistics.keys():
            self.statistics[key] += other[key]
        
        return self

    def clear(self):
        for key in self.statistics.keys():
            self.statistics[key] = 0

    def total(self):
        sum = 0
        for key in self.statistics.keys():
            sum += self.statistics[key]
        
        return sum
