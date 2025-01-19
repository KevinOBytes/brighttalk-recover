"""Custom exceptions for BrightTalk-Recover."""


class BTRecoverError(Exception):
    """Base exception for BrightTalk-Recover."""

    pass


class FFmpegNotFoundError(BTRecoverError):
    """Raised when ffmpeg is not found or not executable."""

    pass


class URLValidationError(BTRecoverError):
    """Raised when URL validation fails."""

    pass


class DownloadError(BTRecoverError):
    """Raised when download fails."""

    pass
