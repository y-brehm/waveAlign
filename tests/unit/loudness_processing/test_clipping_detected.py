import unittest

from wavealign.loudness_processing.clipping_detected import clipping_detected


class TestClippingDetected(unittest.TestCase):
    def test_check_for_clipping_true(self):
        self.assertTrue(clipping_detected(-1, -10, -8))
        self.assertTrue(clipping_detected(-0.1, -15, -14))

    def test_check_for_clipping_false(self):
        self.assertFalse(clipping_detected(-1, -10, -12))
        self.assertFalse(clipping_detected(-0.1, -15, -16))
