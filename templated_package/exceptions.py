class BaseException(Exception):
    """ 
    The base class for all exceptions.
    It is not meant to be directly instantiated, unlike specific exceptions here below.
    """

class NotYetImplementedException(BaseException):
    """
    This exception is raised when attempting to reach code that has not yet been implemented.
    """