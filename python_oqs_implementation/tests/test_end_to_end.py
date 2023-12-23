import unittest
from typing import Callable
from python_oqs_implementation.oqs.engine import oqs_engine
from python_oqs_implementation.oqs.constants.types import ErrorTypeStrings as ETS
from python_oqs_implementation.oqs.utils.shortcuts import get_oqs_type
from .utils import get_test_function_name


class TestLanguageEngine(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual({"results": {"value": 10, "type": "Integer"}}, oqs_engine(expression="2 * 5"))

    def test_divide(self):
        self.assertEqual({"results": {"value": 5, "type": "Decimal"}}, oqs_engine(expression="10 / 2"))

    def test_modulo(self):
        self.assertEqual({"results": {"value": 1, "type": "Integer"}}, oqs_engine(expression="9 % 2"))

    def test_string_concatenation(self):
        self.assertEqual(
            {"results": {"value": "Hello World", "type": "String"}}, oqs_engine(expression='"Hello " + "World"')
        )

    def test_string_repetition(self):
        self.assertEqual(
            {"results": {"value": "repeatrepeat", "type": "String"}}, oqs_engine(expression='"repeat" * 2')
        )

    def test_boolean_comparison(self):
        self.assertEqual({"results": {"value": False, "type": "Boolean"}}, oqs_engine(expression="true == false"))
        self.assertEqual({"results": {"value": True, "type": "Boolean"}}, oqs_engine(expression="true != false"))

    def test_list_concatenation(self):
        self.assertEqual({"results": {"value": [1, 2, 3, 4], "type": "List"}}, oqs_engine(expression="[1, 2] + [3, 4]"))

    def test_list_subtraction(self):
        self.assertEqual({"results": {"value": [1, 2, 4], "type": "List"}}, oqs_engine(expression="[1, 2, 3, 4] - [3]"))

    def test_kvs_concatenation(self):
        self.assertEqual(
            {"results": {"value": {"a": 1, "b": 2, "c": 3}, "type": "KVS"}},
            oqs_engine(expression='{ "a": 1, "b": 2 } + { "c": 3 }')
        )

    def test_add_function(self):
        self.assertEqual({"results": {"value": 3, "type": "Integer"}}, oqs_engine(expression="ADD(1, 2)"))

    def test_complex_expression(self):
        self.assertEqual(
            {"results": {"value": "valid", "type": "String"}},
            oqs_engine(expression='IF(LEN("test") == 4, "valid", "invalid")')
        )
        self.assertEqual(
            {"results": {"value": 25, "type": "Integer"}},
            oqs_engine(expression='ADd(length([5, 10, ***[4, 3, "HEllo:,"]]), 20)')
        )

    def test_addition(self):
        self.assertEqual({"results": {"value": 3, "type": "Integer"}}, oqs_engine(expression="1 + 2"))

    def test_subtraction(self):
        self.assertEqual({"results": {"value": 3, "type": "Integer"}}, oqs_engine(expression="5 - 2"))

    def test_exponentiation(self):
        self.assertEqual({"results": {"value": 8, "type": "Integer"}}, oqs_engine(expression="2 ** 3"))

    def test_string_subtraction(self):
        self.assertEqual({"results": {"value": "re", "type": "String"}}, oqs_engine(expression='"remove" - "move"'))

    def test_list_add_function(self):
        self.assertEqual(
            {"results": {"value": [1, 2, 3, 4], "type": "List"}}, oqs_engine(expression='ADD([1, 2], [3, 4])')
        )

    def test_kvs_add_function(self):
        self.assertEqual(
            {"results": {"value": {"a": 1, "b": 2}, "type": "KVS"}},
            oqs_engine(expression='ADD({ "a": 1 }, { "b": 2 })')
        )

    def test_integer_function(self):
        self.assertEqual({"results": {"value": 3, "type": "Integer"}}, oqs_engine(expression='INTEGER(3.5)'))

    def test_decimal_function(self):
        self.assertEqual({"results": {"value": 42.0, "type": "Decimal"}}, oqs_engine(expression='DECIMAL("42")'))

    def test_string_function(self):
        self.assertEqual(
            {"results": {"value": "[1, 2, 3]", "type": "String"}}, oqs_engine(expression='STRING([1, 2, 3])')
        )

    def test_boolean_function(self):
        self.assertEqual({"results": {"value": True, "type": "Boolean"}}, oqs_engine(expression='BOOLEAN(1)'))

    def test_keys_function(self):
        self.assertEqual(
            {"results": {"value": ["name", "type"], "type": "List"}},
            oqs_engine(expression='KEYS({ "name": "OQS", "type": "script" })')
        )

    def test_values_function(self):
        self.assertEqual(
            {"results": {"value": ["OQS", "script"], "type": "List"}},
            oqs_engine(expression='VALUES({ "name": "OQS", "type": "script" })')
        )

    def test_complex_if_expression(self):
        self.assertEqual(
            {"results": {"value": "valid", "type": "String"}},
            oqs_engine(expression='IF(LEN("test") == 4, "valid", "invalid")')
        )

    def test_complex_add_expression(self):
        self.assertEqual({"results": {"value": 10, "type": "Integer"}}, oqs_engine(expression='ADD(***[1, 2, 3, 4])'))

    def test_unpacked_integer(self):
        self.assertEqual({"results": {"value": 5, "type": "Integer"}}, oqs_engine(expression='INTEGER(***["5"])'))

    def test_kvs_expansion(self):
        self.assertEqual(
            {"results": {"value": {"key1": "value1", "key2": "value2"}, "type": "KVS"}},
            oqs_engine(expression='{***{"key1": "value1"}, ***{"key2": "value2"}}')
        )

    def test_string_embedded_expression(self):
        self.assertEqual(
            {"results": {"value": "8 is the answer", "type": "String"}},
            oqs_engine(expression='<{3 + 5}> is the answer', string_embedded=True)
        )


class TestLanguageEngineAdvanced(unittest.TestCase):
    def setUp(self):
        self.leer: Callable = self.language_engine_expected_result
        self.cases: dict[str, list[dict[str, any]]] = {}

    def language_engine_expected_result(
            self,
            expression: str,
            expected_value: any = None,
            expected_type: str = None,
            variables: dict[str, any] | None = None,
            string_embedded: bool = False,
            expect_error: bool = False,
            error_message: str = None,
    ):
        if expected_type is None:
            expected_type: str = get_oqs_type(expected_value)
        results: dict[str, any] = oqs_engine(
            expression=expression, variables=variables, string_embedded=string_embedded
        )
        expected_results: dict[str, any] = {
            "error": {"type": expected_type, "message": error_message}
        } if expect_error else {"results": {"value": expected_value, "type": expected_type}}
        function_name: str = get_test_function_name()
        if function_name not in self.cases:
            self.cases[function_name] = []
        self.cases[function_name].append(
            {
                "input": {"expression": expression, "variables": variables, "string_embedded": string_embedded},
                "output": expected_results
            }
        )
        self.assertEqual(expected_results, results)

    def test_basic(self):
        self.leer("2 * 5 + 3", 13)
        self.leer('"Hello " + name', "Hello World", variables={"name": "World"})
        self.leer('ADD(1, 2, 3)', 6)
        self.leer('SUBTRACT(10, LENGTH(name))', 7, variables={"name": "OQS"})
        self.leer("MULTIPLY(3, ***numbers)", 12, variables={"numbers": [2, 2]})
        self.leer('DECIMAL(STRING(number))', 123.0, variables={"number": 123})
        self.leer('IF(LEN(text) > 5, "Long", "Short")', "Short", variables={"text": "Hello"})
        self.leer('{***kvs1, ***kvs2}', {"a": 1, "b": 2}, variables={"kvs1": {"a": 1}, "kvs2": {"b": 2}})
        self.leer('SUM([1, 2, 3]) + SUM([4, 5, 6])', 21)
        self.leer('STRING(ADD(1, 2, 3)) + " is the sum"', "6 is the sum")

    def test_numerical_and_string_operations(self):
        self.leer('3 ** 2 + LEN("test")', 13)
        self.leer('STRING(5.0 * 2) - ".0"', "10")

    def test_list_and_kvs_operations(self):
        self.leer('[1, 2, 3] + REVERSE([4, 5, 6])', [1, 2, 3, 6, 5, 4])
        self.leer('KEYS({ "a": 1, "b": 2 }) + VALUES({ "a": 1, "b": 2 })', ["a", "b", 1, 2])
        self.leer('SUM([1, 2, 3, 4])', 10)
        self.leer('MAX(***numbers)', 5, variables={"numbers": [1, 2, 3, 4, 5]})

    def test_complex_nested_expressions(self):
        self.leer('IF(LEN(name) > 5, SUBTRACT(LEN(name), 3), ADD(LEN(name), 2))', 6, variables={"name": "Scripting"})
        self.leer('STRING(ADD(***[INTEGER("1"), DECIMAL("2.5"), 3]))', "6.5")

    def test_error_handling(self):
        self.leer(
            'DIVIDE(10, 0)',
            expected_type=ETS.DIVISION_BY_ZERO,
            expect_error=True,
            error_message='Division by zero results in undefined.'
        )

    def test_string_embedded_expressions(self):
        self.leer('<{ADD(1, 2)}> + <{MULTIPLY(3, 4)}>', "3 + 12", string_embedded=True)
        self.leer(
            'Result is <{IF(LEN(text) == 5, "five", "not five")}>.',
            'Result is five.',
            variables={"text": "Hello"},
            string_embedded=True
        )

    def test_advanced_scenarios(self):
        self.leer('UNIQUE([***numbers, ***REVERSE(numbers)])', [1, 2, 3], variables={"numbers": [1, 2, 3]})
        self.leer('REMOVE_ITEM([1, 2, 3, 2, 3, 3], 3, 2)', [1, 2, 2, 3])
        self.leer(
            'UPDATE(kvs, "newKey", IF(ACCESS(kvs, "key") == 5, 10, 0))',
            {"key": 5, "newKey": 10},
            variables={"kvs": {"key": 5}}
        )

    def test_advanced_numerical_operations(self):
        self.leer('MODULO(15, 4) + DIVIDE(20, 5)', 7.0)
        self.leer('EXPONENTIATE(ADD(2, 3), SUBTRACT(5, 2))', 125)

    def test_complex_string_manipulation(self):
        self.leer('STRING(LEN("Hello")) + " characters"', "5 characters")
        self.leer('"Start-" + MULTIPLY("A", 3) + "-End"', "Start-AAA-End")

    def test_list_and_kvs_combinations(self):
        self.leer('APPEND(UNIQUE([1, 2, 2, 3]), MAX(***[4, 5, 6]))', [1, 2, 3, 6])
        self.leer('ACCESS({***{"key": "value"}, ***{"another": SUM([1, 2, 3])}}, "another")', 6)

    def test_function_calls_with_complex_arguments(self):
        self.leer('STRING(ADD(INTEGER("3"), DECIMAL("2.5"), MULTIPLY(2, 2)))', "9.5")
        self.leer('BOOLEAN(LEN("test") == 4)', True)

    def test_nested_and_conditional_expressions(self):
        self.leer('IF(LEN(name) > 5, LEN(name), "short")', 15, variables={"name": "OpenQuickScript"})
        self.leer('STRING(ADD(1, IF(true, 2, 3)))', "3")

    def test_error_scenarios_and_edge_cases(self):
        self.leer(
            'DIVIDE("10", 2)',
            expected_type=ETS.TYPE,
            expect_error=True,
            error_message="Cannot divide type 'String' by type 'Integer'."
        )

    def test_string_embedded_and_unpacking_expressions(self):
        self.leer(
            "<{ADD(1, LEN(text))}> is the length", "6 is the length", variables={"text": "Hello"}, string_embedded=True
        )
        self.leer(
            '{ "sum": "<{SUM([***numbers])}>", "max": "<{MAX(***numbers)}>" }',
            '{ "sum": "10", "max": "4" }',
            variables={"numbers": [1, 2, 3, 4]},
            string_embedded=True
        )

    def test_complex_function_calls_and_list_manipulations(self):
        self.leer('REMOVE_ITEM([1, 2, 3, 4, 5], ADD(2, 1))', [1, 2, 4, 5])
        self.leer('APPEND(numbers, MULTIPLY(LENGTH(numbers), 2))', [1, 2, 3, 6], variables={"numbers": [1, 2, 3]})

    def test_kvs_and_list_integration(self):
        self.leer(
            'KEYS({ "name": "OQS", "version": "0.1" }) + VALUES({ "name": "OQS", "version": "0.1" })',
            ["name", "version", "OQS", "0.1"]
        )
        self.leer(
            'UPDATE(kvs, "new", ADD(ACCESS(kvs, "existing"), 10))',
            {"existing": 5, "new": 15},
            variables={"kvs": {"existing": 5}}
        )

    def test_advanced_mathematical_operations(self):
        self.leer('MODULO(ADD(15, 5), DIVIDE(20, 2))', 0.0)
        self.leer('EXPONENTIATE(SUBTRACT(10, 2), 3)', 512)

    def test_string_manipulation_and_comparisons(self):
        self.leer('LEN("Concatenate") == 11', True)
        self.leer('STRING(LEN("Concatenate") == 11)', "true")
        self.leer('IF("text" - "t" == "ex", "Correct", "Incorrect")', "Correct")

    def test_complex_list_operations(self):
        self.leer('REVERSE(APPEND(numbers, SUM(numbers)))', [6, 3, 2, 1], variables={"numbers": [1, 2, 3]})

    def test_function_usage_with_nested_calls(self):
        self.leer('MULTIPLY(DECIMAL("3.5"), INTEGER(2.5))', 7.0)
        self.leer('ADD(STRING(LEN("abc")), STRING(LEN("def")))', "33")

    def test_conditional_expressions_with_functions(self):
        self.leer('IF(LEN(name) < 5, LEN(name), SUBTRACT(LEN(name), 2))', 4, variables={"name": "Script"})
        self.leer('IF(true, SUM([1,2,3]), MULTIPLY(2,3))', 6)

    def test_error_handling_scenarios(self):
        self.leer(
            'ADD("5", 10)', expected_type=ETS.TYPE, expect_error=True, error_message="Cannot add 'String' and 'Integer'"
        )
        self.leer('SUBTRACT([1, 2, 3], 1)', expected_type=ETS.TYPE, expect_error=True)

    def test_string_embedded_and_complex_unpacking(self):
        self.leer(
            "<{MULTIPLY(2, LEN(text))}> is twice the length",
            "8 is twice the length",
            variables={"text": "Test"},
            string_embedded=True
        )
        self.leer('SUM([***numbers, ***REVERSE(numbers)])', 12, variables={"numbers": [1, 2, 3]})

    def test_advanced_function_calls_and_kvs_manipulations(self):
        self.leer("REMOVE_ITEM(UNIQUE(numbers), MIN(***numbers), 1)", [2, 3], variables={"numbers": [1, 2, 1, 3]})
        self.leer(
            'UPDATE(kvs, "total", SUM(***VALUES(kvs)))',
            {"a": 1, "b": 2, "total": 3},
            variables={"kvs": {"a": 1, "b": 2}}
        )

    def test_complex_evaluation_involving_multiple_data_types(self):
        self.leer('STRING(ADD(***[1, 2, 3], LEN("[1, 2, 3]")))', "9")
        self.leer("SUM([1, 2, 3]) == STRING(6)", False)

