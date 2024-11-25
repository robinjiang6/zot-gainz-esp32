# Author: Robin Jiang
# Date: 11/6/24
# Description: Additional datatype to be used with bluetooth low energy

class Reading:
    def __init__(self,
                 max_length = 10,
                 ):
        """
        self.rolling_heading: float, average of past max_length readings
        self.rolling_pitch: float, average of past max_length readings
        self.rolling_roll: float, average of past max_length readings
        self.max_length: integer, limits number of readings stored at a time
        self.readings: deque (queue) that stores readings 
        """
        self.rolling_heading = 0
        self.rolling_pitch = 0
        self.rolling_roll = 0
        self.max_length = max_length
        self.readings = []

    def add_reading(self, heading: float, pitch: float, roll: float):
        """Appends reading to self.readings"""
        reading = (heading, pitch, roll)
        self.readings.append(reading)
        if len(self.readings) > self.max_length:
            self.readings.popleft()
        self.rolling_heading = sum(reading[0] for reading in self.readings)/len(self.readings)
        self.rolling_pitch = sum(reading[1] for reading in self.readings)/len(self.readings)
        self.rolling_roll = sum(reading[2] for reading in self.readings)/len(self.readings)

    
    def get_reading(self):
        """Returns the rolling averages"""
        return self.rolling_heading, self.rolling_pitch, self.rolling_roll

    def print(self):
        """Prints the current reading"""
        print(f"Heading: {pretty_print(self.rolling_heading)}, Pitch: {pretty_print(self.rolling_pitch)}, Roll: {pretty_print(self.rolling_roll)}")
    
    def __len__(self):
        return len(self.readings)
    

def pretty_print(data: float):
    add = ""
    if data >= 0:
        add = " "
    if abs(data) < 10:
        data = f"{data:.5f}"
    elif abs(data) < 100:
        data = f"{data:.4f}"
    else:
        data = f"{data:.3f}"
    return add + data