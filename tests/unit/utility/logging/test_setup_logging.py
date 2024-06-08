# import unittest
# import mock
#
# from wavealign.utility.logging.setup_logging import setup_logging
#
#
# class TestSetupLogging(unittest.TestCase):
#     @mock.patch("logging.config.dictConfig")
#     @mock.patch("wavealign.data_collection.logging_configuration.create_logging_config")
#     def test_setup_logging(self, mock_create_logging_config, mock_config_dictConfig):
#         output_path = "/path/to/directory"
#         verbose = False
#
#         setup_logging(output_path, verbose)
#
#         mock_create_logging_config.assert_called_once_with(output_path, verbose)
#         mock_config_dictConfig.assert_called_once_with(
#             mock_create_logging_config.return_value
#         )
