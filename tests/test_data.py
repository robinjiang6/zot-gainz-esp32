# unittests for data.py

import unittest
from resources.data import Reading

class TestData(unittest.TestCase):
    def test_initializes_with_zero_readings(self):
        x = Reading()
        self.assertEqual(len(x), 0)

    def test_popping_raises_index_error_with_zero_readings(self):
        x = Reading()
        self.assertRaises(x.pop(), IndexError)

if __name__ == "__main__":
    unittest.main()