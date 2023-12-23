import inspect
import unittest
from python_oqs_implementation.oqs.engine import oqs_engine
from python_oqs_implementation.oqs.utils.shortcuts import get_oqs_type


def get_test_function_name() -> str:
    stack: list = inspect.stack()
    for frame in stack[1:]:
        if frame.function.startswith('test_'):
            return str(frame.function)


def language_engine_expected_result(
        test_class: unittest.TestCase,
        expression: str,
        expected_value: any = None,
        expected_type: str = None,
        variables: dict[str, any] | None = None,
        string_embedded: bool = False,
        expect_error: bool = False,
        error_message: str = None,
) -> None:
    if expected_type is None:
        expected_type: str = get_oqs_type(expected_value)
    results: dict[str, any] = oqs_engine(
        expression=expression, variables=variables, string_embedded=string_embedded
    )
    expected_results: dict[str, any] = {
        "error": {"type": expected_type, "message": error_message}
    } if expect_error else {"results": {"value": expected_value, "type": expected_type}}
    function_name: str = get_test_function_name()
    if function_name not in test_class.cases:
        test_class.cases[function_name] = []
    test_class.cases[function_name].append(
        {
            "input": {"expression": expression, "variables": variables, "string_embedded": string_embedded},
            "output": expected_results
        }
    )
    test_class.assertEqual(expected_results, results)
