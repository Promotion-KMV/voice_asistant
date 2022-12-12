"""Speech Recognition Exceptions."""


class SpeechRecognitionException(Exception):
    """Basic Speech Recognition Exception."""

    ...


class YandexServiceException(SpeechRecognitionException):
    """Yandex exceptions."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class YandexSpeechRecognitionException(YandexServiceException):
    ...


class YandexIAMException(YandexServiceException):
    ...
