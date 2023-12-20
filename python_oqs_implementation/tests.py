import unittest
from python_oqs_implementation.engine import oqs_engine


class TestLanguageEngine(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(oqs_engine(expression="2 * 5"), {"results": {"value": 10, "type": "Integer"}})

    def test_divide(self):
        self.assertEqual(oqs_engine(expression="10 / 2"), {"results": {"value": 5, "type": "Integer"}})

    def test_modulo(self):
        self.assertEqual(oqs_engine(expression="9 % 2"), {"results": {"value": 1, "type": "Integer"}})

    def test_string_concatenation(self):
        self.assertEqual(
            oqs_engine(expression='"Hello " + "World"'), {"results": {"value": "Hello World", "type": "String"}}
        )

    def test_string_repetition(self):
        self.assertEqual(
            oqs_engine(expression='"repeat" * 2'), {"results": {"value": "repeatrepeat", "type": "String"}}
        )

    def test_boolean_comparison(self):
        self.assertEqual(
            oqs_engine(expression="true == false"), {"results": {"value": False, "type": "Boolean"}}
        )
        self.assertEqual(
            oqs_engine(expression="true != false"), {"results": {"value": True, "type": "Boolean"}}
        )

    def test_list_concatenation(self):
        self.assertEqual(oqs_engine(expression="[1, 2] + [3, 4]"), {"results": {"value": [1, 2, 3, 4], "type": "List"}})

    def test_list_subtraction(self):
        self.assertEqual(oqs_engine(expression="[1, 2, 3, 4] - [3]"), {"results": {"value": [1, 2, 4], "type": "List"}})

    def test_kvs_concatenation(self):
        self.assertEqual(
            oqs_engine(expression='{ "a": 1, "b": 2 } + { "c": 3 }'),
            {"results": {"value": {"a": 1, "b": 2, "c": 3}, "type": "KVS"}}
        )

    def test_add_function(self):
        self.assertEqual(oqs_engine(expression="ADD(1, 2)"), {"results": {"value": 3, "type": "Integer"}})

    def test_complex_expression(self):
        self.assertEqual(
            oqs_engine(expression='IF(LEN("test") == 4, "valid", "invalid")'),
            {"results": {"value": "valid", "type": "String"}}
        )

    def test_addition(self):
        self.assertEqual(oqs_engine(expression="1 + 2"), {"results": {"value": 3, "type": "Integer"}})

    def test_subtraction(self):
        self.assertEqual(oqs_engine(expression="5 - 2"), {"results": {"value": 3, "type": "Integer"}})

    def test_exponentiation(self):
        self.assertEqual(oqs_engine(expression="2 ** 3"), {"results": {"value": 8, "type": "Integer"}})

    def test_string_subtraction(self):
        self.assertEqual(
            oqs_engine(expression='"remove" - "move"'), {"results": {"value": "re", "type": "String"}}
        )

    def test_list_add_function(self):
        self.assertEqual(
            oqs_engine(expression='ADD([1, 2], [3, 4])'), {"results": {"value": [1, 2, 3, 4], "type": "List"}}
        )

    def test_kvs_add_function(self):
        self.assertEqual(
            oqs_engine(expression='ADD({ "a": 1 }, { "b": 2 })'),
            {"results": {"value": {"a": 1, "b": 2}, "type": "KVS"}}
        )

    def test_integer_function(self):
        self.assertEqual(oqs_engine(expression='INTEGER(3.5)'), {"results": {"value": 3, "type": "Integer"}})

    def test_decimal_function(self):
        self.assertEqual(oqs_engine(expression='DECIMAL("42")'), {"results": {"value": 42.0, "type": "Decimal"}})

    def test_string_function(self):
        self.assertEqual(
            oqs_engine(expression='STRING([1, 2, 3])'), {"results": {"value": "[1, 2, 3]", "type": "String"}}
        )

    def test_boolean_function(self):
        self.assertEqual(oqs_engine(expression='BOOLEAN(1)'), {"results": {"value": True, "type": "Boolean"}})

    def test_keys_function(self):
        self.assertEqual(
            oqs_engine(expression='KEYS({ "name": "OQS", "type": "script" })'),
            {"results": {"value": ["name", "type"], "type": "List"}}
        )

    def test_values_function(self):
        self.assertEqual(
            oqs_engine(expression='VALUES({ "name": "OQS", "type": "script" })'),
            {"results": {"value": ["OQS", "script"], "type": "List"}}
        )

    def test_complex_if_expression(self):
        self.assertEqual(
            oqs_engine(expression='IF(LEN("test") == 4, "valid", "invalid")'),
            {"results": {"value": "valid", "type": "String"}}
        )

    def test_complex_add_expression(self):
        self.assertEqual(
            oqs_engine(expression='ADD(*[1, 2, 3, 4])'),
            {"results": {"value": 10, "type": "Integer"}}
        )

    def test_unpacked_integer(self):
        self.assertEqual(
            oqs_engine(expression='INTEGER(*["5"])'),
            {"results": {"value": 5, "type": "Integer"}}
        )

    def test_kvs_expansion(self):
        self.assertEqual(
            oqs_engine(expression='{**{"key1": "value1"}, **{"key2": "value2"}}'),
            {"results": {"value": {"key1": "value1", "key2": "value2"}, "type": "KVS"}}
        )

    def test_string_embedded_expression(self):
        self.assertEqual(
            oqs_engine(expression='<{3 + 5}> is the answer', string_embedded=True),
            {"results": {"value": "8 is the answer", "type": "String"}}
        )


if __name__ == '__main__':
    unittest.main()
