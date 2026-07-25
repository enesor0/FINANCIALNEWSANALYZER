"""Errors that application callers can handle without knowing an adapter."""


class DataProviderUnavailable(RuntimeError):
    """Raised when an external provider cannot return usable live data."""
