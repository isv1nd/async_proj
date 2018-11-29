class BaseAuthenticationException(Exception):
    pass


class CredentialsWereNotProvidedException(BaseAuthenticationException):
    pass


class InvalidTokenException(BaseAuthenticationException):
    pass


class InvalidCredentialsException(BaseAuthenticationException):
    pass


class UserIsInactiveException(BaseAuthenticationException):
    pass
