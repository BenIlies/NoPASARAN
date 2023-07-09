class ParsingError(Exception):
    """
    Exception raised for errors that occur during parsing.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message):
        """
        Initializes a ParsingError object.

        Args:
            message (str): Explanation of the error.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the ParsingError.

        Returns:
            str: String representation of the error.
        """
        return f"ParsingError: {self.message}"