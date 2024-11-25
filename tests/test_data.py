# unittests for data.py

import unittest
from data import Reading

class TestData(unittest.TestCase):
    def test_initializes_with_zero_readings(self):
        x = Reading()
        self.assertEqual(len(x), 0)
    
    def test_can_add_reading(self):
        x = Reading()
        x.add_reading(0, 1.1, 2.2)
        self.assertEqual(len(x), 1)

if __name__ == "__main__":
    unittest.main()