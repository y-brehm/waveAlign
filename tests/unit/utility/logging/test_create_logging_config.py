# import unittest
# import mock
#
# from wavealign.utility.logging.create_logging_config import create_logging_config
#
#
# class TestCreateLoggingConfig(unittest.TestCase):
#     @mock.patch("os.path.join", return_value="dummy_path")
#     def test_create_logging_config_nonverbose(self, mock_os_path_join):
#         output_path = "/path/to/directory"
#         verbose = False
#
#         create_logging_config(output_path, verbose)
#
#         mock_os_path_join.assert_called_once_with(output_path, "wavealign.log")
