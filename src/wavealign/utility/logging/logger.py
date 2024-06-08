import logging.config
import yaml
import os

from wavealign.utility.logging.warning_status_singleton import WarningStatusSingleton


class Logger:
    def __init__(self, output_path: str, verbose: bool):
        self.__logfile_name = "wavealign.log"
        self.__logging_config = self.__create_logging_config(output_path, verbose)
        logging.config.dictConfig(self.__logging_config)

    def __create_logging_config(self, output_path: str, verbose: bool) -> dict:
        self.__log_file_path = os.path.join(output_path, self.__logfile_name)
        if verbose:
            log_level = "DEBUG"
        else:
            log_level = "INFO"

        with open("wavealign/utility/logging/logging_config.yaml", "r") as config_file:
            logging_config = yaml.safe_load(config_file)

            logging_config["handlers"]["warning"]["filename"] = self.__log_file_path
            logging_config["handlers"]["debug"]["filename"] = self.__log_file_path
            logging_config["loggers"]["root"]["level"] = log_level

        return logging_config

    def output_logfile_warning(self) -> None:
        warning_status = WarningStatusSingleton()

        if (
            not os.path.exists(self.__log_file_path)
            or not warning_status.get_warning_counts()
        ):
            return

        print(
            f"\nSome files were not processed successfully. "
            f"A log file at {self.__log_file_path} was written."
        )
