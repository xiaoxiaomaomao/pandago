from SessionGroup import *
class Helper:
    @staticmethod
    def traversalWithId(container, operate, ids):
        sessionIds = None
        for item in container:
            if ids != None:
                sessionIds = [id for id in ids if item.isSessionExisted(id)]
                if len(sessionIds) == 0:
                    continue
            operate(item, sessionIds)
            
    @staticmethod
    def traversal(container, operator):
        for item in container:
            if operator(item) == False:
                break
    
    @staticmethod
    def traversalWithParam(container, operator, param):
        for item in container:
            if operator(item, param) == False:
                break
    
    @staticmethod     
    def stop(group, sessionIds):
        group.stop(sessionIds)
        
    @staticmethod 
    def start(group, sessionIds):
        group.go(sessionIds)
        
    @staticmethod 
    def remove(group, sessionIds):
        group.remove(sessionIds)
    