from core import Filter
class filterComposite(Filter.Filter):
    def __init__(self):
        self.filters = []
    
    def removeFilter(self, filter):
        if filter in self.filters:
            self.filters.remove(filter)
    
    def addFilter(self,filter):
        self.filters.append(filter)
    
    def doFilter(self, rawData):
        for filter in self.filters:
            rawData = filter.doFilter(rawData)
        return rawData