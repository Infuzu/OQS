from .constants.types import ErrorTypeStrings as ETS


class OQSBaseError(Exception):
    def __init__(
            self, readable_name: str = ETS.BASE, message: str = "An error occurred while evaluating your expression!"
    ) -> None:
        super().__init__(message)
        self.readable_name: str = readable_name


class OQSInvalidArgumentQuantityError(OQSBaseError):
    def __init__(self, function_name: str, expected_min: int, expected_max: int, actual: int) -> None:
        message: str = (
            f"Function '{function_name}' expected at least {expected_min} with a max of {expected_max} arguments, "
            f"but got {actual}"
        )
        super().__init__(readable_name=ETS.INVALID_ARGUMENT_QUANTITY, message=message)


class OQSSyntaxError(OQSBaseError):
    def __init__(self, message: str, specific_name: str = ETS.SYNTAX) -> None:
        super().__init__(readable_name=specific_name, message=message)


class OQSTypeError(OQSBaseError):
    def __init__(self, message: str) -> None:
        super().__init__(readable_name=ETS.TYPE, message=message)


class OQSUndefinedVariableError(OQSBaseError):
    def __init__(self, variable_name: str) -> None:
        message: str = f"The variable {variable_name} is not defined."
        super().__init__(readable_name=ETS.UNDEFINED_VARIABLE, message=message)


class OQSUndefinedFunctionError(OQSBaseError):
    def __init__(self, function_name: str) -> None:
        message: str = f"The function '{function_name}' is not a valid function."
        super().__init__(readable_name=ETS.UNDEFINED_FUNCTION, message=message)


class OQSFunctionEvaluationError(OQSBaseError):
    def __init__(self, function_name: str, message: str) -> None:
        full_message: str = f"Error in function '{function_name}': {message}"
        super().__init__(readable_name=ETS.FUNCTION_EVALUATION, message=full_message)


class OQSDivisionByZeroError(OQSBaseError):
    def __init__(self) -> None:
        super().__init__(readable_name=ETS.DIVISION_BY_ZERO, message="Division by zero results in undefined.")


class OQSUnexpectedCharacterError(OQSSyntaxError):
    def __init__(self, message: str) -> None:
        super().__init__(specific_name=ETS.UNEXPECTED_CHARACTER, message=message)


class OQSMissingExpectedCharacterError(OQSSyntaxError):
    def __init__(self, message: str) -> None:
        super().__init__(specific_name=ETS.MISSING_EXPECTED_CHARACTER, message=message)
