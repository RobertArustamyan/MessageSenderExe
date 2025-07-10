class CookieExtractorError(Exception):
    """Base exception for cookie extractor."""
    pass

class LoginError(CookieExtractorError):
    """Exception raised when login fails."""
    pass

class CookieExportError(CookieExtractorError):
    """Exception raised when cookie export fails."""
    pass

class DriverInitializationError(CookieExtractorError):
    """Exception raised when driver initialization fails."""
    pass