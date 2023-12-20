class OQSBaseError(Exception):
    def __init__(
            self,
            readable_name: str = "OQS Base Error",
            message: str = "An error occurred while evaluating your expression!"
    ) -> None:
        super().__init__(message)
        self.readable_name: str = readable_name


class OQSInvalidArgumentQuantityError(OQSBaseError):
    def __init__(self, function_name: str, expected_min: int, expected_max: int, actual: int) -> None:
        message: str = (
            f"Function '{function_name}' expected at least {expected_min} with a max of {expected_max} arguments, "
            f"but got {actual}"
        )
        super().__init__(readable_name="Invalid Argument Quantity Error", message=message)


class OQSSyntaxError(OQSBaseError):
    def __init__(self, message: str) -> None:
        super().__init__(readable_name="Syntax Error", message=message)


class OQSTypeError(OQSBaseError):
    def __init__(self, message: str) -> None:
        super().__init__(readable_name="Type Error", message=message)


class OQSUndefinedVariableError(OQSBaseError):
    def __init__(self, variable_name: str) -> None:
        message: str = f"The variable {variable_name} is not defined."
        super().__init__(readable_name="Undefined Variable Error", message=message)


class OQSUndefinedFunctionError(OQSBaseError):
    def __init__(self, function_name: str) -> None:
        message: str = f"The function '{function_name}' is not a valid function."
        super().__init__(readable_name="Undefined Function Error", message=message)


class OQSFunctionEvaluationError(OQSBaseError):
    def __init__(self, function_name: str, message: str) -> None:
        full_message: str = f"Error in function '{function_name}': {message}"
        super().__init__(readable_name="Function Evaluation Error", message=full_message)
