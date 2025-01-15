# Author: Robin Jiang
# Date: 11/6/24
# Description: Additional datatype to be used with ESP Now
import json
from collections import deque

class Reading:
    def __init__(self, name = "generic",
                 reading_length = 10,
                 max_readings = 10,
                 contains_heading = False):
        """
        reading_length:     how many readings are averaged for each stored reading
        max_readings:        how many readings can be stored. 10 readings w/ 10 average reading w/10ms between
                            each readings = 1000ms of data stored at a time, each reading 100ms apart
        self.data:          dict, stores name and average heading/pitch/roll data
        self.max_length:    int, limits number of readings stored at a time
        self.readings:      deque that stores readings 
        """
        self.data = {
                        "n": name,
                        "h": [],
                        "p": [],
                        "r": []
                    }
        if not contains_heading:
            del self.data['h']
        self.max_readings = max_readings
        self.reading_length = reading_length
        self.readings = deque([], reading_length)
        self.count = 0

    def add_reading(self, heading: int, pitch: int, roll: int):
        """Appends reading to self.readings and updates rolling averages"""
        # rounds inputted data to nearest integer
        reading = (round(heading), round(pitch), round(roll))
        if self.count == self.reading_length:
            if 'h' in self.data:
                self.data["h"].append(sum(reading[0] for reading in self.readings)//len(self.readings))
            self.data["p"].append(sum(reading[1] for reading in self.readings)//len(self.readings))
            self.data["r"].append(sum(reading[2] for reading in self.readings)//len(self.readings))
            self.count = 0
            if len(self.data["p"]) > self.max_readings:
                if 'h' in self.data:
                    self.data["h"].pop(0)
                self.data["p"].pop(0)
                self.data["r"].pop(0)
        self.readings.append(reading)
        self.count += 1

    
    def get_reading(self) -> tuple:
        """Returns the rolling averages as a tuple"""
        heading = 0
        if 'h' in self.data:
            heading = self.data['h']
        return heading, self.data['p'], self.data['r']

    def prepare_reading(self):
        """Formats reading into json string format to send in ESPNOW"""
        return json.dumps(self.data)
    
    @staticmethod
    def decipher_reading(reading: str):
        """Decifers a reading in json format, for when receiving data in ESPNOW"""
        return json.loads(reading)

    def print(self):
        """Prints the current reading"""
        heading = 0
        if 'h' in self.data:
            heading = self.data['h']
        print(f"Heading: {pretty_print(heading)}, Pitch: {pretty_print(self.data['p'][-1])}, Roll: {pretty_print(self.data['r'][-1])}")
    
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