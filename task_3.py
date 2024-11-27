import math
import unittest
import numpy as np


def time_to_cyclic_features(hour):

    angle = (2 * math.pi * hour) / 24
    return math.sin(angle), math.cos(angle)


def cyclic_time_difference(hour1, hour2):

    sin1, cos1 = time_to_cyclic_features(hour1)
    sin2, cos2 = time_to_cyclic_features(hour2)
    # Calculate angular difference
    delta_angle = math.acos(cos1 * cos2 + sin1 * sin2)
    # Convert back to hours
    return (delta_angle / (2 * math.pi)) * 24


# Unit Test Class
class TestCyclicFeatures(unittest.TestCase):
    def test_time_to_cyclic_features(self):

        hour = 0
        sine, cosine = time_to_cyclic_features(hour)
        self.assertAlmostEqual(sine, 0.0, delta=1e-6)
        self.assertAlmostEqual(cosine, 1.0, delta=1e-6)

        hour = 6
        sine, cosine = time_to_cyclic_features(hour)
        self.assertAlmostEqual(sine, 1.0, delta=1e-6)
        self.assertAlmostEqual(cosine, 0.0, delta=1e-6)

        hour = 18
        sine, cosine = time_to_cyclic_features(hour)
        self.assertAlmostEqual(sine, -1.0, delta=1e-6)
        self.assertAlmostEqual(cosine, 0.0, delta=1e-6)

    def test_cyclic_time_difference(self):

        self.assertAlmostEqual(cyclic_time_difference(23, 1), 2.0, delta=1e-6)
        self.assertAlmostEqual(cyclic_time_difference(1, 23), 2.0, delta=1e-6)
        self.assertAlmostEqual(cyclic_time_difference(12, 18), 6.0, delta=1e-6)
        self.assertAlmostEqual(cyclic_time_difference(18, 6), 12.0, delta=1e-6)

    def test_cyclic_time_difference_same_time(self):

        self.assertAlmostEqual(cyclic_time_difference(5, 5), 0.0, delta=1e-6)
        self.assertAlmostEqual(cyclic_time_difference(0, 0), 0.0, delta=1e-6)

    def test_cyclic_time_difference_boundary(self):

        self.assertAlmostEqual(cyclic_time_difference(0, 24), 0.0, delta=1e-6)
        self.assertAlmostEqual(cyclic_time_difference(23.5, 0.5), 1.0, delta=1e-6)


if __name__ == "__main__":
    unittest.main()
