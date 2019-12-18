class PiastrixApiException(Exception):
    """Piastrix API Exception.

    Args:
        message (:obj:`str`): Exception description.
        error_code (:obj:`int`): Error code.
    """

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code
