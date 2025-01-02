# Author: Robin Jiang
# Date: 11/6/24
# Description: Additional datatype to be used with bluetooth low energy
import json
from collections import deque

class Reading:
    def __init__(self, name = "generic_sensor",
                 max_length = 10,
                 ):
        """
        self.data:          dict, stores name and rolling heading/pitch/roll data
        self.max_length:    int, limits number of readings stored at a time
        self.readings:      deque that stores readings 
        """
        self.data = {
                        "name": name,
                        "heading": 0,
                        "pitch": 0,
                        "roll": 0
                    }
        self.max_length = max_length
        self.readings = deque([], max_length)

    def add_reading(self, heading: int, pitch: int, roll: int):
        """Appends reading to self.readings and updates rolling averages"""
        # rounds inputted data to nearest integer
        reading = (round(heading), round(pitch), round(roll))
        self.readings.append(reading)
        if len(self.readings) > self.max_length:
            self.readings.popleft()
        self.data["heading"] = sum(reading[0] for reading in self.readings)//len(self.readings)
        self.data["pitch"] = sum(reading[1] for reading in self.readings)//len(self.readings)
        self.data["roll"] = sum(reading[2] for reading in self.readings)//len(self.readings)

    
    def get_reading(self) -> tuple:
        """Returns the rolling averages as a tuple"""
        return self.data['heading'], self.data['pitch'], self.data['roll']

    def prepare_reading(self):
        """Formats reading into json string format to send in ESPNOW"""
        return json.dumps(self.data)
    
    @staticmethod
    def decipher_reading(reading: str):
        """Decifers a reading in json format, for when receiving data in ESPNOW"""
        return json.loads(reading)

    def print(self):
        """Prints the current reading"""
        print(f"Heading: {pretty_print(self.data['heading'])}, Pitch: {pretty_print(self.data['pitch'])}, Roll: {pretty_print(self.data['roll'])}")
    
    def __len__(self):
        return len(self.readings)
    

def pretty_print(data: int) -> str:
    add = ""
    if abs(data) < 100:
        add += " "
    if abs(data) < 10:
        add += " "
    if data >= 0:
        add += " "
    return add + str(data)