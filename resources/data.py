# Author: Robin Jiang
# Date: 11/6/24
# Description: Additional datatype with underlying 
# queue to be used with bluetooth low energy

from collections import deque

class Reading:
    def __init__(self,
                 max_length = 50,
                 ):
        """
        self.max_length: integer, limits number of readings stored at a time
        self.readings: deque (queue) that stores readings 
        """
        self.max_length = max_length
        self.readings = deque()

    def append(self, reading: tuple[float, float, float]):
        """Appends reading to self.readings"""
        self.readings.append(reading)
        self._require_less_readings_than_max_length()

    
    def pop(self, num = 1):
        """Returns the oldest num readings in self.readings, popping them as a result.
        If num is greater than 1, returns readings as a list. If num is 1, returns a tuple."""
        if num == 1:
            return self.readings.popleft()
        ret = []
        for _ in num:
            ret.append(self.readings.popleft())
        return ret
    
    def __len__(self):
        return len(self.readings)

    def _require_less_readings_than_max_length(self):
        """Pops old readings if max length is exceeded"""
        while len(self.readings) > self.max_length:
            print(f"too many readings, popping: {self.readings.popleft()}")