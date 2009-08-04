from core import Filter
import string
class LineFilter(Filter.Filter):
    def doFilter(self, rawData):
        return string.split(rawData, "\r\n")