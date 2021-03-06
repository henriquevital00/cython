class InvalidTokenException(Exception):
    """Class responsible for raise exception if an invalid token was identified"""

    def __init__(self, message):
        self.message = f"Invalid token: {message}"
