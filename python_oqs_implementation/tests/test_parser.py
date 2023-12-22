import unittest
from typing import Callable
from python_oqs_implementation.oqs.errors import (
    OQSSyntaxError, OQSUnexpectedCharacterError, OQSMissingExpectedCharacterError
)
from python_oqs_implementation.oqs.parser import OQSParser


class TestSingleTokenizer(unittest.TestCase):
    def setUp(self) -> None:
        self._parser: OQSParser = OQSParser()
        self.tokenize: Callable = self._parser.tokenize_expression

    def test_string(self):
        self.assertEqual(['"string"'], self.tokenize('"string"'))
        self.assertEqual(["'string'"], self.tokenize("'string'"))

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('"string".')

        with self.assertRaises(OQSSyntaxError):
            self.tokenize('"string" "string"')

    def test_variable(self):
        self.assertEqual(['variable'], self.tokenize('variable'))
        self.assertEqual(['vari3ble'], self.tokenize('vari3ble'))
        self.assertEqual(['_variable'], self.tokenize('_variable'))
        self.assertEqual(['varia_ble'], self.tokenize('varia_ble'))
        self.assertEqual(['variable_'], self.tokenize('variable_'))

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('variable.')

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('variable variable')

    def test_integer(self):
        self.assertEqual(['5'], self.tokenize('5'))
        self.assertEqual(['555'], self.tokenize('555'))
        self.assertEqual(['555555'], self.tokenize('555_555'))
        self.assertEqual(['5555555'], self.tokenize('5_555_555'))

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('5s5')

        with self.assertRaises(OQSSyntaxError):
            self.tokenize('5 5')

    def test_decimal(self):
        self.assertEqual(['5.5'], self.tokenize('5.5'))
        self.assertEqual(['5.555555'], self.tokenize('5.555555'))
        self.assertEqual(['0.5'], self.tokenize('.5'))
        self.assertEqual(['5.0'], self.tokenize('5.'))
        self.assertEqual(['555555.5'], self.tokenize('555_555.5'))

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('.')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('55.5s')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('555.5_5')

        with self.assertRaises(OQSSyntaxError):
            self.tokenize('555.55 5.55')

    def test_function(self):
        self.assertEqual(['ADD()'], self.tokenize('ADD()'))
        self.assertEqual(['ADD(variable)'], self.tokenize('ADD(variable)'))
        self.assertEqual(['ADD(variable, variable,variable)'], self.tokenize('ADD(variable, variable,variable)'))
        self.assertEqual(['ADD("string")'], self.tokenize('ADD("string")'))
        self.assertEqual(['ADD(555)'], self.tokenize('ADD(555)'))
        self.assertEqual(['ADD(5.5)'], self.tokenize('ADD(5.5)'))
        self.assertEqual(['ADD(5 5 5 5 )'], self.tokenize('ADD(5 5 5 5 )'))
        self.assertEqual(['ADD(5 + 5)'], self.tokenize('ADD(5 + 5)'))

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('ADD(')

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('ADD(5')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('ADD(5).')

        with self.assertRaises(OQSSyntaxError):
            self.tokenize('ADD(5) 5')

    def test_nested_function(self):
        self.assertEqual(['ADD(ADD(5, ADD(5, 2, 5)), 2)'], self.tokenize('ADD(ADD(5, ADD(5, 2, 5)), 2)'))
        self.assertEqual(['ADD({{{{)'], self.tokenize('ADD({{{{)'))
        self.assertEqual(['ADD([[[[)'], self.tokenize('ADD([[[[)'))

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('ADD((()')

    def test_list(self):
        self.assertEqual(
            ['[5, 5, "string"' + ", 'string', 4, ADD(3, 4), 2]"],
            self.tokenize('[5, 5, "string"' + ", 'string', 4, ADD(3, 4), 2]"),
        )
        self.assertEqual(['[]'], self.tokenize('[]'))

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('[')

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('[5')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('[5].')

        with self.assertRaises(OQSSyntaxError):
            self.tokenize('[5] 5')

    def test_nested_list(self):
        self.assertEqual(['[5, [5, 2], [5, 2, [5, 2, [5, 2]]]]'], self.tokenize('[5, [5, 2], [5, 2, [5, 2, [5, 2]]]]'))
        self.assertEqual(['[((((]'], self.tokenize('[((((]'))
        self.assertEqual(['[{{{{]'], self.tokenize('[{{{{]'))

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('[[[]')

    def test_kvs(self):
        self.assertEqual(['{anything}'], self.tokenize('{anything}'))

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('{')

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('{"string": variable')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('{"string": variable}.')

        with self.assertRaises(OQSSyntaxError):
            self.tokenize('{"string": variable} 5')

    def test_nested_kvs(self):
        self.assertEqual(
            ['{"string": variable, "string2": {"string": variable}}'],
            self.tokenize('{"string": variable, "string2": {"string": variable}}')
        )
        self.assertEqual(['{[[[[}'], self.tokenize('{[[[[}'))
        self.assertEqual(['{((((}'], self.tokenize('{((((}'))

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize('{{}')

    def test_unpacking(self):
        self.assertEqual(['***variable'], self.tokenize('***variable'))
        self.assertEqual(['***{}'], self.tokenize('***{}'))
        self.assertEqual(['***{variable_1:variable_2}'], self.tokenize('***{variable_1:variable_2}'))
        self.assertEqual(['***[]'], self.tokenize('***[]'))
        self.assertEqual(['***[variable]'], self.tokenize('***[variable]'))
        self.assertEqual(['***()'], self.tokenize('***()'))
        self.assertEqual(['***(variable_1)'], self.tokenize('***(variable_1)'))

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('***"string"')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize("***'string'")

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('***1')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('***1.0')

    def operator_test(self, operator: str):
        self.assertEqual(['5', operator,  '3'], self.tokenize(f'5 {operator} 3'))
        self.assertEqual(['"string"', operator,  '3'], self.tokenize(f'"string" {operator} 3'))
        self.assertEqual(['variable', operator, '3'], self.tokenize(f'variable {operator} 3'))
        self.assertEqual(['[]', operator,  '3'], self.tokenize(f'[] {operator} 3'))
        self.assertEqual([f'(5 {operator} 5)', operator,  '3'], self.tokenize(f'(5 {operator} 5) {operator} 3'))
        self.assertEqual(['anything', operator, 'anything'], self.tokenize(f'anything {operator} anything'))
        self.assertEqual(['anything', operator, 'anything'], self.tokenize(f'anything{operator}anything'))
        self.assertEqual(
            ['anything', operator, 'anything', operator, 'anything'],
            self.tokenize(f'anything {operator} anything {operator} anything')
        )
        self.assertEqual(['anything', operator*4, 'anything'], self.tokenize(f'anything {operator*4} anything'))

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize(f'5 {operator} ')

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize(f'5 {operator} 5 {operator}')

        with self.assertRaises(OQSMissingExpectedCharacterError):
            self.tokenize(f'{operator} 5')

    def test_addition(self):
        self.operator_test(operator="+")

    def test_subtraction(self):
        self.operator_test(operator="-")

    def test_division(self):
        self.operator_test(operator="/")

    def test_multiplication(self):
        self.operator_test(operator="*")

    def test_exponentiation(self):
        self.operator_test(operator="**")

    def test_modulation(self):
        self.operator_test(operator="%")

    def test_greater_than(self):
        self.operator_test(operator=">")

    def test_less_than(self):
        self.operator_test(operator="<")

    def test_greater_than_or_equal_to(self):
        self.operator_test(operator=">=")

    def test_less_than_or_equal_to(self):
        self.operator_test(operator="<=")

    def test_equal(self):
        self.operator_test(operator="==")

    def test_not_equal(self):
        self.operator_test(operator="!=")

    def test_strictly_equal(self):
        self.operator_test(operator="===")

    def test_strictly_not_equal(self):
        self.operator_test(operator="!==")

    def test_commas(self):
        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('5, 5')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('variable, variable')

        with self.assertRaises(OQSUnexpectedCharacterError):
            self.tokenize('anything, ')


class TestSeparatorTokenizer(unittest.TestCase):
    def setUp(self) -> None:
        self._parser: OQSParser = OQSParser()
        self.separate: Callable = self._parser.separate_arguments

    def test_no_commas(self):
        self.assertEqual(['5 + 5'], self.separate("5 + 5"))
        self.assertEqual(['5'], self.separate('5'))
        self.assertEqual(['variable'], self.separate('variable'))
        self.assertEqual(['"string"'], self.separate('"string"'))
        self.assertEqual(['ADD(5, 4, 3)'], self.separate('ADD(5, 4, 3)'))

    def test_single_commas(self):
        self.assertEqual(['5 + 5'], self.separate('5 + 5,'))
        self.assertEqual(['5'], self.separate('5,'))
        self.assertEqual(['variable'], self.separate('variable,'))
        self.assertEqual(['"string"'], self.separate('"string",'))
        self.assertEqual(['ADD(5, 4, 3)'], self.separate('ADD(5, 4, 3),'))

    def test_two_commas(self):
        self.assertEqual(['5 + 5', '5 + 5'], self.separate('5 + 5, 5 + 5'))
        self.assertEqual(['5', '5'], self.separate('5, 5'))
        self.assertEqual(['variable', 'variable'], self.separate('variable, variable'))
        self.assertEqual(['"string"', '"string"'], self.separate('"string", "string"'))
        self.assertEqual(['ADD(5, 4, 3)', 'ADD(5, 4, 3)'], self.separate('ADD(5, 4, 3), ADD(5, 4, 3)'))

    def test_multiple_commas(self):
        self.assertEqual(['5 + 5', '5 + 5', '5 + 5'], self.separate('5 + 5, 5 + 5, 5 + 5'))
        self.assertEqual(['5', '5', '5'], self.separate('5, 5, 5'))
        self.assertEqual(['variable', 'variable', 'variable'], self.separate('variable, variable, variable'))
        self.assertEqual(['"string"', '"string"', '"string"'], self.separate('"string", "string", "string"'))
        self.assertEqual(
            ['ADD(5, 4, 3)', 'ADD(5, 4, 3)', 'ADD(5, 4, 3)'], self.separate('ADD(5, 4, 3), ADD(5, 4, 3), ADD(5, 4, 3)')
        )

    def test_commas_no_space(self):
        self.assertEqual(['5 + 5', '5 + 5', '5 + 5'], self.separate('5 + 5,5 + 5,5 + 5'))
        self.assertEqual(['5', '5', '5'], self.separate('5,5,5'))
        self.assertEqual(['variable', 'variable', 'variable'], self.separate('variable,variable,variable'))
        self.assertEqual(['"string"', '"string"', '"string"'], self.separate('"string","string","string"'))
        self.assertEqual(
            ['ADD(5, 4, 3)', 'ADD(5, 4, 3)', 'ADD(5, 4, 3)'], self.separate('ADD(5, 4, 3),ADD(5, 4, 3),ADD(5, 4, 3)')
        )

    def test_trailing_commas(self):
        self.assertEqual(['5 + 5', '5 + 5', '5 + 5'], self.separate('5 + 5, 5 + 5, 5 + 5,'))
        self.assertEqual(['5', '5', '5'], self.separate('5, 5, 5,'))
        self.assertEqual(['variable', 'variable', 'variable'], self.separate('variable, variable, variable,'))
        self.assertEqual(['"string"', '"string"', '"string"'], self.separate('"string", "string", "string",'))
        self.assertEqual(
            ['ADD(5, 4, 3)', 'ADD(5, 4, 3)', 'ADD(5, 4, 3)'], self.separate('ADD(5, 4, 3), ADD(5, 4, 3), ADD(5, 4, 3),')
        )
