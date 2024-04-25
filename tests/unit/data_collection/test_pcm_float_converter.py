import unittest
import mock
from numpy import array, int16, float32
from numpy.testing import assert_almost_equal

from wavealign.data_collection.pcm_float_converter import PcmFloatConverter


class TestPcmFloatConverter(unittest.TestCase):
    def setUp(self):
        self.mock_iinfo = mock.patch(
            "wavealign.data_collection.pcm_float_converter.iinfo"
        ).start()

    def tearDown(self):
        mock.patch.stopall()

    def test_is_pcm_encoded(self):
        self.mock_iinfo.return_value = type("MockInfo", (), {"bits": 16})

        pcm_signal = array([0, 1, 2], dtype=int16)
        float_signal = array([0.0, 1.0, 2.0], dtype=float32)

        converter = PcmFloatConverter()
        self.assertTrue(converter.is_pcm_encoded(pcm_signal))
        self.assertFalse(converter.is_pcm_encoded(float_signal))

    def test_pcm_to_float(self):
        self.mock_iinfo.return_value = type(
            "MockInfo", (), {"bits": 16, "min": -32768, "max": 32767}
        )

        pcm_signal = array([0, 32767, -32768], dtype=int16)
        expected_float_signal = array([0.0, 1.0, -1.0], dtype=float32)
        float_signal = PcmFloatConverter().pcm_to_float(pcm_signal)

        assert_almost_equal(float_signal, expected_float_signal, decimal=4)

    def test_float_to_pcm(self):
        self.mock_iinfo.return_value = type(
            "MockInfo", (), {"bits": 16, "min": -32768, "max": 32767}
        )

        float_signal = array([0.0, 1.0, -1.0], dtype=float32)
        expected_pcm_signal = array([0, 32767, -32768], dtype=int16)
        pcm_signal = PcmFloatConverter().float_to_pcm(float_signal)

        assert_almost_equal(pcm_signal, expected_pcm_signal, decimal=4)
