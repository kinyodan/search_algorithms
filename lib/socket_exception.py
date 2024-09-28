class SocketCommunicationError(Exception):
    """Custom exception for socket communication errors."""
    def __init__(self, message):
        super().__init__(message)
