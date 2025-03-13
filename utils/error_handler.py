import traceback

class ErrorHandler:
    @staticmethod
    def handle_error(error_message, exception_obj=None, critical=False):
        """
        Handles errors by logging them and optionally raising exceptions.
        :param error_message: Custom error message.
        :param exception_obj: Exception object (optional).
        :param critical: If True, raises the exception after logging.
        """
        log_message = f"ERROR: {error_message}"
        
        if exception_obj:
            log_message += f" | Exception: {str(exception_obj)}"
            log_message += f"\nTraceback: {traceback.format_exc()}"  # Captures full error trace
        
        print(log_message)  # Log to console (can be replaced with a file logger)
        
        if critical:
            raise Exception(error_message)
