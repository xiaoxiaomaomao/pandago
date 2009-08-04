"""
    Update the statistic of the status information of session. 
"""
import threading
import time
from core.SessionStatistics import SessionStatistics
class UpdateInterface:
    def update(self, staticstics):
        pass
    
class UpdateStatisticsWorker(threading.Thread):
    SLEEP_TIME = 2
    def __init__(self, master, manager):
        threading.Thread.__init__(self)
        self.master = master
        self.manager = manager
        self.scheduleTime  = UpdateStatisticsWorker.SLEEP_TIME
    
    def setScheduleTime(self, time):
        self.scheduleTime = time
        
    def run(self):
        while True:
            statics = self.manager.getStatistics()
            self.master.update(statics)
            time.sleep(self.scheduleTime)
    