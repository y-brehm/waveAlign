import mock
import unittest
from parameterized import parameterized
import math
import numpy as np

from wavealign.loudness_processing.db_gain_conversion import gain_to_db, db_to_gain


class TestDbGainConversion(unittest.TestCase):
    @mock.patch('wavealign.loudness_processing.db_gain_conversion.np.log10')
    def test_gain_to_db(self, mock_np_log):
        fake_gain = -5
        gain_to_db(fake_gain)
        mock_np_log.assert_called_once_with(fake_gain)

    @parameterized.expand([
        ('base case', 5, 13.979400086720377),
        ('low case', 1, 0),
        ('high case', 30, 29.54242509439325),
        ('zero case', 0, -math.inf),
    ])
    def test_gain_to_db_values(self, _, fake_gain, expected):
        fake_db = gain_to_db(fake_gain)
        np.testing.assert_almost_equal(fake_db, expected)

    @parameterized.expand([
        ('base case', 5, 1.7782794100389228),
        ('low case', 1, 1.1220184543019633),
        ('high case', 30, 31.622776601683793),
        ('zero case', 0, 1),
    ])
    def test_db_to_gain_values(self, _, fake_db, expected):
        fake_gain = db_to_gain(fake_db)
        np.testing.assert_almost_equal(fake_gain, expected)
