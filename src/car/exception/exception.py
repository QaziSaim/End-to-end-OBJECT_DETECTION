import sys
from src.boneFractureDetection.logging.logger import logger


class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error(error_message, error_details)

    def get_detailed_error(self, error_message, error_details):
        _, _, exc_tb = error_details.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return f"Error occurred in script [{file_name}] at line [{line_number}] : {error_message}"

    def __str__(self):
        return self.error_message