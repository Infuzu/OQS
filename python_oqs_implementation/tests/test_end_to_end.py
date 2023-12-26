import datetime
import unittest
from python_oqs_implementation.oqs.constants.types import ErrorTypeStrings as ETS
from .utils import language_engine_expected_result


class TestLanguageEngine(unittest.TestCase):
    def setUp(self):
        self.cases: dict[str, list[dict[str, any]]] = {}

    def leer(self, *args, **kwargs) -> None:
        language_engine_expected_result(self, *args, **kwargs)

    def test_multiply(self):
        self.leer("2 * 5", 10)

    def test_divide(self):
        self.leer("10 / 2", 5)

    def test_modulo(self):
        self.leer("9 % 2", 1)

    def test_logical_and_operator(self):
        self.leer("true & false", False)
        self.leer("1 & 0", False)
        self.leer('"text" & ""', False)

    def test_logical_or_operator(self):
        self.leer("false | true", True)
        self.leer("0 | 1", True)
        self.leer('"" | "text"', True)

    def test_string_concatenation(self):
        self.leer('"Hello " + "World"', "Hello World")

    def test_string_repetition(self):
        self.leer('"repeat" * 2', "repeatrepeat")

    def test_boolean_comparison(self):
        self.leer("true == false", False)
        self.leer("true != false", True)

    def test_list_concatenation(self):
        self.leer("[1, 2] + [3, 4]", [1, 2, 3, 4])

    def test_list_subtraction(self):
        self.leer("[1, 2, 3, 4] - [3]", [1, 2, 4])

    def test_kvs_concatenation(self):
        self.leer('{ "a": 1, "b": 2 } + { "c": 3 }', {"a": 1, "b": 2, "c": 3})

    def test_add_function(self):
        self.leer("ADD(1, 2)", 3)

    def test_complex_expression(self):
        self.leer('IF(LEN("test") == 4, "valid", "invalid")', "valid")
        self.leer('ADd(length([5, 10, ***[4, 3, "HEllo:,"]]), 20)', 25)

    def test_addition(self):
        self.leer("1 + 2", 3)

    def test_subtraction(self):
        self.leer("5 - 2", 3)

    def test_exponentiation(self):
        self.leer("2 ** 3", 8)

    def test_string_subtraction(self):
        self.leer('"remove" - "move"', "re")

    def test_list_add_function(self):
        self.leer('ADD([1, 2], [3, 4])', [1, 2, 3, 4])

    def test_kvs_add_function(self):
        self.leer('ADD({ "a": 1 }, { "b": 2 })', {"a": 1, "b": 2})

    def test_integer_function(self):
        self.leer('INTEGER(3.5)', 3)

    def test_decimal_function(self):
        self.leer('DECIMAL("42")', 42.0)

    def test_string_function(self):
        self.leer('STRING([1, 2, 3])', "[1, 2, 3]")

    def test_boolean_function(self):
        self.leer('BOOLEAN(1)', True)

    def test_keys_function(self):
        self.leer('KEYS({ "name": "OQS", "type": "script" })', ["name", "type"])

    def test_values_function(self):
        self.leer('VALUES({ "name": "OQS", "type": "script" })', ["OQS", "script"])

    def test_complex_if_expression(self):
        self.leer('IF(LEN("test") == 4, "valid", "invalid")', "valid")

    def test_complex_add_expression(self):
        self.leer('ADD(***[1, 2, 3, 4])', 10)

    def test_unpacked_integer(self):
        self.leer('INTEGER(***["5"])', 5)

    def test_kvs_expansion(self):
        self.leer('{***{"key1": "value1"}, ***{"key2": "value2"}}', {"key1": "value1", "key2": "value2"})

    def test_string_embedded_expression(self):
        self.leer('<{3 + 5}> is the answer', "8 is the answer", string_embedded=True)

    def test_datetime_addition(self):
        self.leer(
            'PARSE_TEMPORAL("2023-12-25T10:00:00", "DateTime") + DURATION(0, 1, 0, 0)',
            datetime.datetime(2023, 12, 25, 11, 0, 0)
        )

    def test_date_subtraction(self):
        self.leer(
            'PARSE_TEMPORAL("2023-12-25", "Date") - DURATION(1, 0, 0, 0)', datetime.date(2023, 12, 24)
        )

    def test_time_addition(self):
        self.leer('PARSE_TEMPORAL("10:00:00", "Time") + DURATION(0, 1, 0, 0)', datetime.time(11, 0, 0))

    def test_duration_subtraction(self):
        self.leer(
            'PARSE_TEMPORAL("1 02:00:00", "Duration") - PARSE_TEMPORAL("1 00:30:00", "Duration")',
            datetime.timedelta(hours=1, minutes=30)
        )

    def test_datetime_comparison(self):
        self.leer(
            'PARSE_TEMPORAL("2023-12-24T10:00:00", "DateTime") < PARSE_TEMPORAL("2023-12-25T10:00:00", "DateTime")',
            True
        )

    def test_date_comparison(self):
        self.leer('PARSE_TEMPORAL("2023-12-26", "Date") > PARSE_TEMPORAL("2023-12-25", "Date")', True)


class TestLanguageEngineAdvanced(unittest.TestCase):
    def setUp(self):
        self.cases: dict[str, list[dict[str, any]]] = {}

    def leer(self, *args, **kwargs) -> None:
        language_engine_expected_result(self, *args, **kwargs)

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
        self.leer('<{2 * 5}> stars', "10 stars", string_embedded=True)

    def test_advanced_scenarios(self):
        self.leer('UNIQUE([***numbers, ***REVERSE(numbers)])', [1, 2, 3], variables={"numbers": [1, 2, 3]})
        self.leer('REMOVE_ITEM([1, 2, 3, 2, 3, 3], 3, 2)', [1, 2, 2, 3])
        self.leer(
            'UPDATE(kvs, "newKey", IF(ACCESS(kvs, "key") == 5, 10, 0))',
            {"key": 5, "newKey": 10},
            variables={"kvs": {"key": 5}}
        )
        self.leer('IF(ADD(1, 2) > 2, "Yes", "No")', "Yes")
        self.leer('ADD(SUBTRACT(10, 5), MULTIPLY(2, 3))', 11)

    def test_advanced_numerical_operations(self):
        self.leer('MODULO(15, 4) + DIVIDE(20, 5)', 7)
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
        self.leer('MODULO(ADD(15, 5), DIVIDE(20, 2))', 0)
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
        self.leer(
            'SUBTRACT([1, 2, 3], 1)',
            expected_type=ETS.TYPE,
            expect_error=True,
            error_message="Cannot subtract 'List' by 'Integer'"
        )

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
            'UPDATE(kvs, "total", SUM(VALUES(kvs)))',
            {"a": 1, "b": 2, "total": 3},
            variables={"kvs": {"a": 1, "b": 2}}
        )

    def test_complex_evaluation_involving_multiple_data_types(self):
        self.leer('STRING(ADD(***[1, 2, 3], LEN("[1, 2, 3]")))', "15")
        self.leer("SUM([1, 2, 3]) == STRING(6)", False)

    def test_order_of_operations(self):
        self.leer("1 + 2 * 3", 7)
        self.leer("1 * 2 + 3", 5)
        self.leer("(1 + 2) * 3", 9)
        self.leer("2 ** 3 * 4", 32)
        self.leer("2 * 3 ** 2", 18)
        self.leer("18 / 2 * 3", 27)
        self.leer("18 / (2 * 3)", 3)
        self.leer("4 + 3 - 2", 5)
        self.leer("4 - 3 + 2", 3)
        self.leer("4 * (2 + 3)", 20)
        self.leer("4 * 2 + 3", 11)
        self.leer("4 + 2 * 3", 10)
        self.leer("5 + 6 / 3 - 1", 6)
        self.leer("5 - 6 / 3 + 1", 4)

    def test_type_interactions(self):
        self.leer('ADD(5, 2.5)', 7.5)
        self.leer('ADD("Hello ", "World")', "Hello World")
        self.leer('SUBTRACT([1, 2, 3], [2])', [1, 3])
        self.leer('ADD({"a": 1}, {"b": 2})', {"a": 1, "b": 2})

    def test_unpacking_and_kvs_expansion(self):
        self.leer('ADD(***[1, 2, 3], ***[4, 5, 6])', 21)
        self.leer('{***{"a": 1}, ***{"b": 2}}', {"a": 1, "b": 2})

    def test_error_scenarios(self):
        self.leer(
            'ADD(1, "two")',
            expected_type=ETS.TYPE,
            expect_error=True,
            error_message="Cannot add 'Integer' and 'String'")
        self.leer(
            'DIVIDE(1, 0)',
            expected_type=ETS.DIVISION_BY_ZERO,
            expect_error=True,
            error_message="Division by zero results in undefined."
        )


class TestOQSFunctions(unittest.TestCase):
    def setUp(self):
        self.cases: dict[str, list[dict[str, any]]] = {}

    def leer(self, *args, **kwargs) -> None:
        language_engine_expected_result(self, *args, **kwargs)

    def test_add_numbers(self):
        self.leer('ADD(1, 2)', 3)

    def test_add_strings(self):
        self.leer('ADD("Hello", " World")', "Hello World")

    def test_add_lists(self):
        self.leer('ADD([1, 2], [3, 4])', [1, 2, 3, 4])

    def test_add_kvs(self):
        self.leer('ADD({"a": 1}, {"b": 2})', {"a": 1, "b": 2})

    def test_subtract_numbers(self):
        self.leer('SUBTRACT(5, 3)', 2)

    def test_subtract_strings(self):
        self.leer('SUBTRACT("hello", "lo")', "hel")

    def test_subtract_lists(self):
        self.leer('SUBTRACT([1, 2, 3], [3])', [1, 2])

    def test_multiply_numbers(self):
        self.leer('MULTIPLY(3, 2)', 6)

    def test_multiply_string(self):
        self.leer('MULTIPLY("ab", 3)', "ababab")

    def test_divide_numbers(self):
        self.leer('DIVIDE(10, 2)', 5)

    def test_divide_by_zero(self):
        self.leer(
            'DIVIDE(5, 0)',
            expected_type=ETS.DIVISION_BY_ZERO,
            expect_error=True,
            error_message='Division by zero results in undefined.'
        )

    def test_exponentiate(self):
        self.leer('EXPONENTIATE(2, 3)', 8)

    def test_modulo(self):
        self.leer('MODULO(10, 3)', 1)

    def test_less_than(self):
        self.leer('LESS_THAN(1, 2, 3)', True)
        self.leer('LESS_THAN(1, 3, 2)', False)

    def test_greater_than(self):
        self.leer('GREATER_THAN(3, 2, 1)', True)
        self.leer('GREATER_THAN(3, 1, 2)', False)

    def test_less_than_or_equal(self):
        self.leer('LESS_THAN_OR_EQUAL(1, 2, 2)', True)
        self.leer('LESS_THAN_OR_EQUAL(2, 2, 1)', False)

    def test_greater_than_or_equal(self):
        self.leer('GREATER_THAN_OR_EQUAL(3, 2, 2)', True)
        self.leer('GREATER_THAN_OR_EQUAL(2, 2, 3)', False)

    def test_equals(self):
        self.leer('EQUALS(2, 2, 2)', True)
        self.leer('EQUALS(2, 2, 3)', False)

    def test_not_equals(self):
        self.leer('NOT_EQUALS(2, 3, 4)', True)
        self.leer('NOT_EQUALS(2, 2, 2)', False)

    def test_strictly_equals(self):
        self.leer('STRICTLY_EQUALS("2", "2", "2")', True)
        self.leer('STRICTLY_EQUALS("2", "2", 2)', False)

    def test_strictly_not_equals(self):
        self.leer('STRICTLY_NOT_EQUALS("2", "3", 2)', True)
        self.leer('STRICTLY_NOT_EQUALS("2", "2", "2")', False)

    def test_integer_conversion(self):
        self.leer('INTEGER(3.5)', 3)

    def test_decimal_conversion(self):
        self.leer('DECIMAL("42")', 42.0)

    def test_string_conversion(self):
        self.leer('STRING([1, 2, 3])', "[1, 2, 3]")

    def test_boolean_conversion(self):
        self.leer('BOOLEAN(1)', True)

    def test_and_function(self):
        self.leer('AND(true, 1, "text")', True)
        self.leer('AND(true, 0)', False)
        self.leer('AND(false, "non-empty string")', False)

    def test_or_function(self):
        self.leer('OR(false, 0, null, "text")', True)
        self.leer('OR(false, 0, "")', False)
        self.leer('OR(null, 0, false, "")', False)

    def test_not_function(self):
        self.leer('NOT(true)', False)
        self.leer('NOT(false)', True)
        self.leer('NOT(0)', True)
        self.leer('NOT(1)', False)
        self.leer('NOT("")', True)
        self.leer('NOT("text")', False)
        self.leer('NOT(null)', True)

    def test_keys_function(self):
        self.leer('KEYS({"name": "OQS", "type": "script"})', ["name", "type"])

    def test_values_function(self):
        self.leer('VALUES({"name": "OQS", "type": "script"})', ["OQS", "script"])

    def test_unique_function(self):
        self.leer('UNIQUE([1, 2, 2, 3])', [1, 2, 3])

    def test_reverse_function(self):
        self.leer('REVERSE([1, 2, 3])', [3, 2, 1])

    def test_max_function(self):
        self.leer('MAX(1, 3, 2)', 3)

    def test_min_function(self):
        self.leer('MIN(1, 3, 2)', 1)

    def test_sum_function(self):
        self.leer('SUM([1, 2, 3])', 6)

    def test_length_function(self):
        self.leer('LENGTH("Hello")', 5)

    def test_append_function(self):
        self.leer('APPEND([1, 2], 3)', [1, 2, 3])

    def test_update_function(self):
        self.leer('UPDATE({"a": 1}, "b", 2)', {"a": 1, "b": 2})

    def test_remove_item_function(self):
        self.leer('REMOVE_ITEM([1, 2, 3, 2, 3, 3], 3, 2)', [1, 2, 2, 3])

    def test_access_function(self):
        self.leer('ACCESS({"a": 1, "b": 2}, "b")', 2)

    def test_if_function(self):
        self.leer('IF(1 > 2, "Yes", "No")', "No")

    def test_type_function(self):
        self.leer('TYPE(5)', "Integer")

    def test_is_type_function(self):
        self.leer('IS_TYPE(5, "number")', True)

    def test_try_function(self):
        self.leer('TRY(1/0, "Division By Zero Error", "Infinity")', "Infinity")

    def test_range_function(self):
        self.leer('RANGE(1, 4)', [1, 2, 3])

    def test_for_map_function(self):
        self.leer('FOR([1, 2, 3], "item", item * 2)', [2, 4, 6])

    def test_raise_function(self):
        self.leer(
            'RAISE("Custom Error", "An error occurred")',
            expected_type=ETS.CUSTOM,
            expect_error=True,
            error_message="An error occurred"
        )

    def test_filter_list(self):
        self.leer('FILTER([1, 2, 3, 4], "x", x > 2)', [3, 4])

    def test_filter_kvs(self):
        self.leer('FILTER({"a": 1, "b": 2, "c": 3}, "value", value == 2)', {"b": 2})

    def test_sort_list_ascending(self):
        self.leer('SORT([4, 1, 3, 2], "x", x)', [1, 2, 3, 4])

    def test_sort_list_descending(self):
        self.leer('SORT([4, 1, 3, 2], "x", x, true)', [4, 3, 2, 1])

    def test_flatten_list(self):
        self.leer('FLATTEN([[1, 2], [3, 4], [5]])', [1, 2, 3, 4, 5])

    def test_slice_list(self):
        self.leer('SLICE([1, 2, 3, 4, 5], 1, 3)', [2, 3])

    def test_slice_string(self):
        self.leer('SLICE("Hello World", 0, 5)', "Hello")

    def test_in_list(self):
        self.leer('IN(3, [1, 2, 3, 4])', True)

    def test_in_kvs(self):
        self.leer('IN("b", {"a": 1, "b": 2, "c": 3})', True)

    def test_not_in_list(self):
        self.leer('IN("z", [1, 2, 3, 4])', False)

    def test_not_in_kvs(self):
        self.leer('IN("d", {"a": 1, "b": 2, "c": 3})', False)

    def test_date_function(self):
        self.leer('DATE(2023, 12, 25)', datetime.date(2023, 12, 25))

    def test_time_function(self):
        self.leer('TIME(10, 30, 0)', datetime.time(10, 30, 0))

    def test_datetime_function(self):
        self.leer('DATETIME(2023, 12, 25, 10, 30, 0)', datetime.datetime(2023, 12, 25, 10, 30, 0))

    def test_duration_function(self):
        self.leer('DURATION(0, 1, 2, 30)', datetime.timedelta(hours=1, minutes=2, seconds=30))

    def test_format_temporal_function(self):
        self.leer('FORMAT_TEMPORAL(PARSE_TEMPORAL("2023-12-25T10:30:00", "DateTime"), "%Y-%m-%d")', "2023-12-25")

    def test_parse_temporal_function(self):
        self.leer('PARSE_TEMPORAL("2023-12-25T10:30:00", "DateTime")', datetime.datetime(2023, 12, 25, 10, 30, 0))
