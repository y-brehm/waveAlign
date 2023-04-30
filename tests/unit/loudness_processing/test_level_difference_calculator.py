import mock
import unittest
from parameterized import parameterized

from wavealign.loudness_processing.level_difference_calculator import LevelDifferenceCalculator


class TestLevelDifferenceCalculator(unittest.TestCase):

    @parameterized.expand([
        ('louder target than input', -12, -10, 1.258925, 2),
        ('louder input than target', -10, -12, 0.794328, -2),
        ('no loudness difference', -12, -12, 0, 0),
        ('zero case', 0, 0, 0, 0)
    ])
    @mock.patch('wavealign.loudness_processing.level_difference_calculator.DbGainConverter.db_to_gain')
    def test_calculate_gain_difference_to_target(
            self,
            test_case,
            fake_input_lufs,
            fake_lufs_target,
            fake_output_gain,
            fake_output_level,
            mock_db_to_gain
    ):
        mock_db_to_gain.return_value = fake_output_gain

        fake_output = LevelDifferenceCalculator().calculate_level_difference_to_target_in_db(
            fake_input_lufs, fake_lufs_target
        )

        mock_db_to_gain.assert_called_once_with(fake_output_level)
        self.assertEqual(fake_output, fake_output_gain)
