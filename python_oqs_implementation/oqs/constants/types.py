class ValueTypeStrings:
    INTEGER: str = "Integer"
    DECIMAL: str = "Decimal"
    STRING: str = "String"
    LIST: str = "List"
    KVS: str = "KVS"
    BOOLEAN: str = "Boolean"
    NULL: str = "Null"
    UNKNOWN: str = "Unknown"


class ErrorTypeStrings:
    BASE: str = "OQS Base Error"
    INVALID_ARGUMENT_QUANTITY: str = "Invalid Argument Quantity Error"
    SYNTAX: str = "Syntax Error"
    TYPE: str = "Type Error"
    UNDEFINED_VARIABLE: str = "Undefined Variable Error"
    UNDEFINED_FUNCTION: str = "Undefined Function Error"
    FUNCTION_EVALUATION: str = "Function Evaluation Error"
    DIVISION_BY_ZERO: str = "Division By Zero Error"
    UNEXPECTED_CHARACTER: str = "Unexpected Character Error"
    MISSING_EXPECTED_CHARACTER: str = "Missing Expected Character Error"
