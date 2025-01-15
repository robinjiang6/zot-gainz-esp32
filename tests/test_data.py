# unittests for data.py

import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from resources.data import Reading

class TestData(unittest.TestCase):
    def test_initializes_with_zero_readings(self):
        x = Reading()
        self.assertEqual(len(x), 0)
    
    def test_can_add_reading(self):
        x = Reading()
        x.add_reading(0, 1, 2)
        self.assertEqual(len(x), 1)

    def test_can_add_ten_readings(self):
        x = Reading()
        for i in range(10):
            x.add_reading(i, 2 * i, 3 * i)
            self.assertEqual(len(x), i + 1)
    
    def test_rolling_average_one_reading(self):
        x = Reading()
        x.add_reading(1, 2, 3)
        readings = x.get_reading()
        self.assertEqual(readings[0], 1)
        self.assertEqual(readings[1], 2)
        self.assertEqual(readings[2], 3)

    def test_rolling_average_two_reading(self):
        x = Reading()
        x.add_reading(1, 2, 3)
        x.add_reading(3, 4, 5)
        readings = x.get_reading()
        self.assertEqual(readings[0], 2)
        self.assertEqual(readings[1], 3)
        self.assertEqual(readings[2], 4)
    
    def test_rolling_average_ten_reading(self):
        x = Reading()
        for i in range(10):
            x.add_reading(i, i, i)
        readings = x.get_reading()
        for i in range(3):
            self.assertEqual(readings[i], sum(_ for _ in range(10))//10)
    
    def test_add_eleven_removes_one_reading(self):
        x = Reading()
        for i in range(11):
            x.add_reading(1, 1, 1)
        self.assertEqual(len(x), 10)
    
    def test_add_fifteen_updates_rolling_average(self):
        x = Reading()
        for i in range(10):
            x.add_reading(1, 1, 1)
        self.assertEqual(x.get_reading(), (1, 1, 1))
        for i in range(5):
            x.add_reading(3, 3, 3)
        self.assertEqual(x.get_reading(), (2, 2, 2))

    def test_prepare_reading(self):
        x = Reading(name="test_sensor")
        x.add_reading(1, 1, 1)
        self.assertEqual(x.prepare_reading(), '{"name": "test_sensor", "heading": 1, "pitch": 1, "roll": 1}')

    def test_decipher_reading(self):
        y = Reading.decipher_reading('{"name": "test_sensor", "heading": 1, "pitch": 1, "roll": 1}')
        self.assertEqual(y, {"name": "test_sensor", "heading": 1, "pitch": 1, "roll": 1})


if __name__ == "__main__":
    unittest.main()