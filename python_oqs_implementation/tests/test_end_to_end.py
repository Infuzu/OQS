import unittest
from python_oqs_implementation.oqs.engine import oqs_engine


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
