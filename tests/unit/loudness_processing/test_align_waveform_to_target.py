import unittest
import numpy as np
from parameterized import parameterized

from wavealign.loudness_processing.align_waveform_to_target import (
    align_waveform_to_target,
)

test_cases = [
    (
        np.array([0.1, -0.2, 0.3, -0.4]),
        -10,
        -5,
        np.array([0.17782794, -0.35565588, 0.53348382, -0.71131176]),
    ),
    (
        np.array([-0.1, 0.2, -0.3, 0.4]),
        -5,
        -10,
        np.array([-0.05623413, 0.11246826, -0.16870239, 0.22493652]),
    ),
    (
        np.array([0.1, -0.2, 0.3, -0.4]),
        0,
        0,
        np.array([0.1, -0.2, 0.3, -0.4]),
    ),
]


class TestAlignWaveformToTarget(unittest.TestCase):
    @parameterized.expand(test_cases)
    def test_align_waveform_to_target(
        self, audio_data, original_audio_level, target_level, expected_output
    ):
        aligned_waveform = align_waveform_to_target(
            audio_data, original_audio_level, target_level
        )

        self.assertIsInstance(aligned_waveform, np.ndarray)
        self.assertEqual(aligned_waveform.shape, audio_data.shape)
        np.testing.assert_almost_equal(aligned_waveform, expected_output, decimal=5)
