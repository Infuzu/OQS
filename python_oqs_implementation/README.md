# Python Implementation of OQS (Open Quick Script)
## Introduction
`OQS` or `Open Quick Script` is a streamlined and system-neutral expression language designed for universal adaptability. It excels in processing fundamental types and operations and can interpret expressions, optionally accompanied by a dictionary, map, or JSON of variables, to produce consistent and logical outcomes.

The `OQS` Python Implementation was built following the [`OQS Specification`](https://github.com/Infuzu/OQS/blob/main/oqs-specification.md) located at in the [main repository]().




## Installation
### Prerequisites
- Python 3.10+ 
- pip package manager



### Installing OQS
To install the Python implementation of OQS, run the following command:

```bash
pip install oqs
```




## Usage
### Basic Usage
```python
from oqs import oqs_engine


# Simple expression evaluation
result: dict[str, dict[str, any]] = oqs_engine(expression="2 + 2")
print(result)


# Expression with variables
result: dict[str, dict[str, any]] = oqs_engine(expression="a + b", variables={"a": 1, "b": 2})
print(result)
```



### Advanced Usage
`OQS` supports complex operations, including lists, string manipulations, and custom functions. Here's an example of using `OQS` with more advanced features including evaluating multiple expressions:

```python
from oqs import (oqs_engine, ExpressionInput)


# Evaluating multiple expressions at once
multi_expressions: list[ExpressionInput] = [
    ExpressionInput(expression="1 + 2"),
    ExpressionInput(expression="a - b", variables={"a": 5, "b": 3}),
    ExpressionInput(expression="<{2 * c}>", variables={"c": 4}, string_embedded=True)
]
results: dict[str, dict[str, any]] = oqs_engine(evaluate_multiple=True, expression_inputs=multi_expressions)
print(results)
```



### Error Handling
The `OQS` engine provides detailed error messages for various error types, including syntax errors, type errors, and undefined variables. Here's how to handle errors gracefully:

```python
from oqs import oqs_engine


result: dict[str, dict[str, any]] = oqs_engine(expression="invalid syntax")
if "error" in result:
    print("Error encountered:", result["error"]["message"])
else:
    print(result)
```



### Built-in Functions
- `ADD(argument1, argument2, ...)` - Adds Numbers, concatenates Strings, merges Lists or merges KVSs:
  - **Inputs**: 
    - **Amount**: A minimum of two inputs with no maximum.
    - **Types**: All input types must be of the same type being one of the following:
      - `Number`
      - `Temporal`
      - `String`
      - `List`
      - `KVS`
  - **Outputs**: The same type that the inputs were. If one of the inputs was a `Decimal`, it will return a `Decimal`.
- `SUBTRACT(argument1, argument2)` - Subtracts numbers or removes instances from strings/lists:
  - **Inputs**:
    - **Amount**: Exactly two inputs required.
      - **Types**:
        - For numbers: Both `Number`. 
        - For strings/lists: Both `String` or `List`.
        - For temporal: First argument should be a `Temporal` and the second argument should be a `Duration`.
  - **Outputs**: The same type as the inputs.
- `MULTIPLY(argument1, argument2, ...)` - Multiplies numbers or repeats strings/lists:
  - **Inputs**:
    - **Amount**: A minimum of two inputs with no maximum.
    - **Types**: Either all `Number` or the first `String`/`List` and the rest `Number`.
  - **Outputs**: The same type as the first input.
- `DIVIDE(argument1, argument2)` - Divides the first number by the second:
  - **Inputs**:
    - **Amount**: Exactly two inputs.
    - **Types**: Both inputs must be `Number`.
    - **Error Handling**: Raises an error if the second argument is zero.
  - **Outputs**: `Number`.
- `EXPONENTIATE(base, exponent)` - Raises a number to the power of another:
  - **Inputs**:
    - **Amount**: Exactly two inputs.
    - **Types**: Both inputs must be `Number`. 
  - **Outputs**: `Number`.
- `MODULO(number1, number2)` - Calculates the remainder of division:
  - **Inputs**:
    - **Amount**: Exactly two inputs.
    - **Types**: Both inputs must be `Number`.
  - **Outputs**: `Number`.
- `LESS_THAN(argument1, argument2, ...)` - Compares if each preceding argument is less than its following argument:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: All inputs must be `Number` or all inputs must be of the same `Temporal` subtype.
  - **Outputs**: `Boolean` - Returns `true` if each argument is less than the next one, otherwise `false`.
- `GREATER_THAN(argument1, argument2, ...)` - Compares if each preceding argument is greater than its following argument:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: All inputs must be `Number` or all inputs must be of the same `Temporal` subtype.
  - **Outputs**: `Boolean` - Returns `true` if each argument is greater than the next one, otherwise `false`.
- `LESS_THAN_OR_EQUAL(argument1, argument2, ...)` - Compares if each preceding argument is less than or equal to its following argument:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: All inputs must be `Number` or all inputs must be of the same `Temporal` subtype.
  - **Outputs**: `Boolean` - Returns `true` if each argument is less than or equal to the next one, otherwise `false`.
- `GREATER_THAN_OR_EQUAL(argument1, argument2, ...)` - Compares if each preceding argument is greater than or equal to its following argument:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: All inputs must be `Number` or all inputs must be of the same `Temporal` subtype.
  - **Outputs**: `Boolean` - Returns `true` if each argument is greater than or equal to the next one, otherwise `false`.
- `EQUALS(argument1, argument2, ...)` - Compares if all arguments are equal:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: Any types, but all must be of the same type.
  - **Outputs**: `Boolean` - Returns `true` if all arguments are equal, otherwise `false`.
- `NOT_EQUALS(argument1, argument2, ...)` - Compares if any of the arguments are not equal:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: Any types, but all must be of the same type.
  - **Outputs**: `Boolean` - Returns `true` if any argument is not equal to the others, otherwise `false`.
- `STRICTLY_EQUALS(argument1, argument2, ...)` - Compares if all arguments are strictly equal (identical in type and value):
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: Any types, but all must be of the same type.
  - **Outputs**: `Boolean` - Returns `true` if all arguments are strictly equal, otherwise `false`.
- `STRICTLY_NOT_EQUALS(argument1, argument2, ...)` - Compares if any of the arguments are strictly not equal (different in type or value):
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: Any types, but all must be of the same type.
  - **Outputs**: `Boolean` - Returns `true` if any argument is strictly not equal to the others, otherwise `false`.
- `AND(argument1, argument2, ...)` - Performs a logical AND operation on all provided arguments:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: Any types, evaluated for their truthiness.
  - **Outputs**: `Boolean` - Returns `true` if all arguments are truthy, otherwise `false`.
  - **Examples**:
    - **Input**: `AND(true, 1, "text")` **Output**: `true`
    - **Input**: `AND(true, 0)` **Output**: `false`
- `OR(argument1, argument2, ...)` - Performs a logical OR operation on all provided arguments:
  - **Inputs**:
    - **Amount**: Two or more inputs.
    - **Types**: Any types, evaluated for their truthiness.
  - **Outputs**: `Boolean` - Returns `true` if at least one argument is truthy, otherwise `false`.
  - **Examples**:
    - **Input**: `OR(false, 0, null, "text")` **Output**: `true`
    - **Input**: `OR(false, 0, "")` **Output**: `false`
- `NOT(argument)` - Performs a logical NOT operation on the provided argument:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: Any type, evaluated for its truthiness.
  - **Outputs**: `Boolean` - Returns `true` if the argument is falsy, otherwise `false`.
  - **Examples**:
    - **Input**: `NOT(true)` **Output**: `false`
    - **Input**: `NOT(0)` **Output**: `true`
    - **Input**: `NOT("text")` **Output**: `false` (since "text" is truthy)
    - **Input**: `NOT(null)` **Output**: `true`
- `INTEGER(argument)` - Converts to an integer representation:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `Decimal`, `String`, `Integer`, or `Boolean`.
  - **Outputs**: `Integer`.
- `DECIMAL(argument)` - Converts to a decimal representation:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `Integer`, `String`, or `Decimal`.
  - **Outputs**: `Decimal`.
- `STRING(argument)` - Converts to a string representation:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: Any single type.
  - **Outputs**: `String`.
- `LIST(argument1, argument2, ...)` - Creates a list from provided arguments:
  - **Inputs**:
    - **Amount**: One or more inputs.
    - **Types**: Any types.
  - **Outputs**: `List`.
- `KVS(key1, value1, key2, value2, ..., keyN, valueN)` - Creates a key-value store:
  - **Inputs**:
    - **Amount**: Even number of inputs (pairs of keys and values).
    - **Types**: Keys must be `String`, values can be any type.
    - **Error Handling**: Raises an error if an odd number of arguments is provided.
  - **Outputs**: `KVS`.
- `BOOLEAN(argument)` / `BOOL(argument)` - Evaluates the truthiness of an argument:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: Any single type.
  - **Outputs**: `Boolean`.Great! To include the `AND` and `OR` functions in the `OQS` language guidelines, we can expand the "Built-in Functions" section. These functions will provide an alternative way to perform logical operations, particularly useful for handling multiple operands or integrating into more complex expressions.
- `KEYS(kvs)` - Retrieves a list of all keys in a KVS:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `KVS`.
  - **Outputs**: `List` of keys.
- `VALUES(kvs)` - Retrieves a list of all values in a KVS:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `KVS`.
  - **Outputs**: `List` of values.
- `UNIQUE(list)` - Returns a list of unique values:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `List`.
  - **Outputs**: `List` containing unique elements.
- `REVERSE(list)` - Reverses the order of a list:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `List`.
  - **Outputs**: `List` in reverse order.
- `MAX(number1, number2, ..., numberN)` - Finds the maximum number:
  - **Inputs**:
    - **Amount**: A minimum of two inputs with no maximum.
    - **Types**: All inputs must be `Number` or all inputs must be of the same `Temporal` subtype.
  - **Outputs**: `Number`.
- `MIN(number1, number2, ..., numberN)` - Finds the minimum number:
  - **Inputs**:
    - **Amount**: A minimum of two inputs with no maximum.
    - **Types**: All inputs must be `Number` or all inputs must be of the same `Temporal` subtype.
  - **Outputs**: `Number`.
- `SUM(list)` - Adds up items in a list:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `List` with all elements of the same base type.
    - **Error Handling**: Raises an error for mixed types.
  - **Outputs**: The sum or concatenation of list items.
- `LENGTH(object)`/`LEN(object)` - Returns the count of items or characters:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `List`, `String`, `Integer`, or `Decimal`.
  - **Outputs**: `Integer`.
- `APPEND(list, item)` - Appends an item to a list:
  - **Inputs**:
    - **Amount**: Exactly two inputs.
    - **Types**: First input must be a `List`, second can be any type. 
  - **Outputs**: `List`.
- `UPDATE(kvs/list, key/index, value)` - Updates a KVS or List with a new value:
  - **Inputs**:
    - **Amount**: Exactly three inputs.
    - **Types**:
      - For lists: First `List`, second `Integer` (index), third any type. 
      - For KVS: First `KVS`, second and third any type (key and value).
    - **Error Handling**: Raises an error if the index does not exist for lists. For KVS, adds or updates the key.
  - **Outputs**: Updated `List` or `KVS`.
- `REMOVE_ITEM(list/kvs, item, max_occurrences=unlimited)` - Removes an item from a list or KVS:
  - **Inputs**:
    - **Amount**: Two or three inputs.
    - **Types**: First input must be `List` or `KVS`, second input is the item to remove, third (optional) is `Integer` for maximum occurrences.
  - **Outputs**: Adjusted `List` or `KVS`.
- `REMOVE(list/kvs, index/key)` - Removes an item from a list or KVS by index or key:
  - **Inputs**:
    - **Amount**: Exactly two inputs.
    - **Types**:
      - For lists: First `List`, second `Integer` (index). 
      - For KVS: First `KVS`, second `String` (key).
    - **Error Handling**: Raises an error if the index does not exist for lists; does not raise an error if a key does not exist in KVS.
  - **Outputs**: Adjusted `List` or `KVS`.
- `ACCESS(list/kvs, index/key, [optional default value])` - Accesses an item in a list or KVS:
  - **Inputs**:
    - **Amount**: Two or three inputs.
    - **Types**:
      - For lists: First `List`, second `Integer` (index). 
      - For KVS: First `KVS`, second `String` (key), third (optional) any type (default value).
    - **Error Handling**: Raises an error if the index does not exist for lists; returns null or default value if the key does not exist in KVS.
  - **Outputs**: The accessed item or default value.
- `IF(condition1, result1, ..., conditionN, resultN, [else_result])` - Evaluates conditions and returns corresponding results:
  - **Inputs**:
    - **Amount**: A minimum of two arguments up to an unlimited amount.
    - **Types**: Alternating between conditions (any type evaluated for truthiness) and results (any type).
  - **Outputs**: The result corresponding to the first true condition or the `else` result.
- `TYPE(argument)` - Determines the type of the given argument:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: Any single type.
  - **Outputs**: A `String` representing the type of the argument, such as "number", "integer", "decimal", "boolean", "list", "string", "function", "null", or "kvs".
  - **Examples**:
    - **Input**: `TYPE(5)` **Output**: `"integer"`
    - **Input**: `TYPE([1, 2, 3])` **Output**: `"list"`
- `IS_TYPE(argument, type_string)` - Evaluates whether the argument's type matches the specified type string:
  - **Inputs**:
    - **Amount**: Exactly two inputs.
    - **Types**: First input of any type, second input a `String`.
    - **Case Insensitivity**: The `type_string` input is case-insensitive.
  - **Outputs**: A `Boolean` indicating the type match.
  - **Superiority Rules**: Types "integer" and "decimal" are considered subtypes of "number". An argument matching "integer" or "decimal" also returns `true` for "number".
  - **Examples**:
    - **Input**: `IS_TYPE(5, "number")` **Output**: `true`
    - **Input**: `IS_TYPE("hello", "string")` **Output**: `true`
- `TRY(expression, error_type1, result1, ..., error_typeN, resultN)` - Attempts to evaluate an expression and handles specific errors with corresponding fallback expressions:
  - **Inputs**:
    - **Amount**: Minimum of three, odd number, no maximum.
    - **Types**: The first input is an expression of any type, followed by alternating `String` error types and their corresponding expressions.
    - **Case Insensitivity**: The `error_type` inputs are case-insensitive.
    - **Superiority Rules**: Error types follow a hierarchy, with specific error types taking precedence over general ones.
  - **Outputs**: The result of the first expression if no error occurs, or the result of the corresponding expression for the first true matching error.
  - **Examples**:
    - **Input**: `TRY(1/0, "Division By Zero Error", "Infinity", "Syntax Error", "Check expression")` **Output**: `"Infinity"`
- `RANGE(start, stop, step)` - Generates a list of integers starting from `start`, ending before `stop`, incrementing by `step`:
  - **Inputs**:
    - **Amount**: Between 1 and 3, all integers.
    - **Defaults**: If only one argument is provided, it is considered as `stop` with `start` defaulting to 0 and `step` defaulting to 1.
  - **Outputs**: A `List` of integers.
  - **Examples**:
    - **Input**: `RANGE(3)` **Output**: `[0, 1, 2]`
    - **Input**: `RANGE(1, 3)` **Output**: `[1, 2]`
    - **Input**: `RANGE(2, 10, 2)` **Output**: `[2, 4, 6, 8]`
- `FOR(list, variable_name, expression)` / `MAP(list, variable_name, expression)`- Iterates over each item in a list, executing an expression for each item:
  - **Inputs**:
    - **Amount**: Exactly three inputs.
    - **Types**: First input must be a `List`, second a `String` for the variable name that will be set to the current item from the list, and third an expression.
    - **Variable**: During each iteration, the variable with the name set in the second argument is set to the current item from the list.
  - **Outputs**: A `List` of the results from evaluating the expression for each list item.
  - **Examples**:
    - **Input**: `FOR([1, 2, 3], FOR_LIST_ITEM * 2)` **Output**: `[2, 4, 6]`
- `RAISE(error_name, error_message)` - Triggers a specified error or creates a custom error:
  - **Inputs**:
    - **Amount**: Exactly two inputs, both `String`.
    - **Types**: First input for the error name, second for the error message.
    - **Custom Error Handling**: If `error_name` is not a predefined error, a custom error with that name is raised.
  - **Outputs**: Raises the specified error.
  - **Examples**:
    - **Input**: `RAISE("Syntax Error", "Invalid syntax")` **Output**: Raises a Syntax Error with the message "Invalid syntax".
    - **Input**: `RAISE("NewError", "Custom error occurred")` **Output**: Raises a custom error named "NewError" with the message "Custom error occurred". 
- `FILTER(list/kvs, variable_name, predicate)` - Filters elements of a `List` or key-value pairs of a `KVS` based on a provided predicate expression:
  - **Inputs**:
    - **list/kvs**: The `List` or `KVS` to be filtered.
    - **variable_name**: A `String` representing the name of the variable that will be assigned each item or key-value pair during evaluation.
    - **predicate**: An expression that returns a `Boolean` value. It is evaluated for each item (or key-value pair in the case of `KVS`) in the `List`/`KVS`.
  - **Outputs**: A new `List` or `KVS` containing only those elements (or key-value pairs) for which the predicate returns `true`.
  - **Examples**:
    - **Input**: `FILTER([1, 2, 3, 4], "x", x > 2)` **Output**: `[3, 4]`
    - **Input**: `FILTER({"a": 1, "b": 2, "c": 3}, "value", value == 2)` **Output**: `{"b": 2}`
- `SORT(list, variable_name, key_expression, [descending=false])` - Sorts a `List` based on a key generated by an expression for each element:
  - **Inputs**:
    - **list**: The `List` to be sorted.
    - **variable_name**: A `String` representing the name of the variable that will be assigned each item during evaluation.
    - **key_expression**: An expression that computes a key for each element in the `List`.
    - **descending** (optional): A `Boolean` indicating whether the sort should be in descending order. Defaults to `false`.
  - **Outputs**: A new `List` sorted based on the keys generated by the `key_expression`.
  - **Examples**:
    - **Input**: `SORT([1, 2, 3, 4], "x", x, true)` **Output**: `[4, 3, 2, 1]`
    - **Input**: `SORT(["apple", "banana", "cherry"], "fruit", LEN(fruit))` **Output**: `["apple", "cherry", "banana"]`
- `FLATTEN(list)` - Flattens a nested `List` (a `List` of `List`s) into a single-level `List`:
  - **Inputs**:
    - **list**: A `List` potentially containing other `List`s as elements.
  - **Outputs**: A new `List` where all elements are not `List`s.
  - **Examples**:
    - **Input**: `FLATTEN([[1, 2], [3, 4], [5]])` **Output**: `[1, 2, 3, 4, 5]`
    - **Input**: `FLATTEN([[["a", "b"], "c"], ["d"]])` **Output**: `["a", "b", "c", "d"]`
- `SLICE(list/string, start, [end])` - Extracts a subsection of a `List` or `String`:
  - **Inputs**:
    - **list/string**: The `List` or `String` from which a subsection is to be extracted.
    - **start**: An `Integer` representing the starting index of the subsection (inclusive).
    - **end** (optional): An `Integer` representing the ending index of the subsection (exclusive). If omitted, the slice includes all elements from the start to the end of the `List`/`String`.
  - **Outputs**: A new `List` or `String` that is a subsection of the input `List`/`String`.
  - **Examples**:
    - **Input**: `SLICE([1, 2, 3, 4, 5], 1, 3)` **Output**: `[2, 3]`
    - **Input**: `SLICE("Hello World", 6)` **Output**: `"World"`
- `IN(value, list/kvs)` - Checks if a given value is present in a `List` or if a given key exists in a `KVS`:
  - **Inputs**:
    - **value**: The value or key to be checked. This can be of any type.
    - **list/kvs**: The `List` or `KVS` to be searched. If a `List` is provided, the function checks for the presence of the value in the `List`. If a `KVS` is provided, the function checks if the value is a key in the `KVS`.
  - **Outputs**: `Boolean`. Returns `true` if the value is found in the `List` or if the value is a key in the `KVS`. Returns `false` otherwise.
  - **Examples**:
    - **Input**: `IN(3, [1, 2, 3, 4])` **Output**: `true`
    - **Input**: `IN("b", {"a": 1, "b": 2, "c": 3})` **Output**: `true`
    - **Input**: `IN("z", [1, 2, 3, 4])` **Output**: `false`
    - **Input**: `IN("d", {"a": 1, "b": 2, "c": 3})` **Output**: `false`
- `DATE(year, month, day)` - Creates a `Date` from specified year, month, and day:
  - **Inputs**:
    - **Amount**: Exactly three inputs.
    - **Types**: All inputs must be `Integer`.
  - **Outputs**: `Date`.
- `TIME(hour, minute, second, [millisecond])` - Creates a `Time` from specified hour, minute, second, and optionally millisecond:
  - **Inputs**:
    - **Amount**: Three or four inputs.
    - **Types**: All inputs must be `Integer`.
  - **Outputs**: `Time`.
- `DATETIME(year, month, day, hour, minute, second, [millisecond])` - Creates a `DateTime` from specified year, month, day, hour, minute, second, and optionally millisecond:
  - **Inputs**:
    - **Amount**: Six or seven inputs.
    - **Types**: All inputs must be `Integer`.
  - **Outputs**: `DateTime`.
- `DURATION(days, hours, minutes, seconds, [milliseconds])` - Creates a `Duration` from specified days, hours, minutes, seconds, and optionally milliseconds:
  - **Inputs**:
    - **Amount**: Four or five inputs.
    - **Types**: All inputs must be `Integer`.
  - **Outputs**: `Duration`.
- `NOW()` - Returns the current UTC `DateTime`:
  - **Outputs**: `DateTime`.
- `TODAY()` - Returns the current UTC `Date`.
   - **Outputs**: `Date`.
- `TIME_NOW()` - Returns the current UTC `Time`.
  - **Outputs**: `Time`.
- `PARSE_TEMPORAL(string, type, [format])` - Converts a `String` to the appropriate `Temporal` type (`DateTime`, `Date`, `Time`, `Duration`), optionally using a specified format. The optional format input will be ignored if the specified type is `Duration`:
  - **Inputs**:
    - **Amount**: One or two inputs.
    - **Types**: First `String`, second `String` one of the Temporal subtypes (case-insensitive), third (optional) `String` (format pattern).
  - **Outputs**: The appropriate `Temporal` type based on the input `String`.
  - **Examples**:
    - **Input**: `PARSE_TEMPORAL("2023-12-25T15:30:00", "DateTime")` **Output**: `DateTime(2023, 12, 25, 15, 30, 0)`
    - **Input**: `PARSE_TEMPORAL("2023-12-25", "Date")` **Output**: `Date(2023, 12, 25)`
    - **Input**: `PARSE_TEMPORAL("15:30:00", "Time")` **Output**: `Time(15, 30, 0)`
    - **Input**: `PARSE_TEMPORAL("1 02:15:30", "Duration")` **Output**: `Duration(1, 2, 15, 30)`
- `FORMAT_TEMPORAL(temporal, format)` - Formats a `Temporal` (`Date`, `Time`, `DateTime`, `Duration`) into a `String` using the specified format:
  - **Inputs**:
    - **Amount**: Exactly two inputs.
    - **Types**: First `Temporal` (`Date`, `Time`, `DateTime`, `Duration`), second `String` (format pattern).
  - **Outputs**: `String`.
- `EXTRACT_DATE(datetime)` - Extracts the `Date` component from a `DateTime`:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `DateTime`.
  - **Outputs**: `Date`.
- `EXTRACT_TIME(datetime)` - Extracts the `Time` component from a `DateTime`:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: `DateTime`.
  - **Outputs**: `Time`.

Function calls are completed by putting the function name first and following it by putting an open parentheses `(` followed by any number of arguments separated by commas `,` and then followed by a closing parentheses `)`.



### Performance Monitoring
Enable performance monitoring to track CPU usage time.

```python
from oqs import oqs_engine


result: dict[str, dict[str, any]] = oqs_engine(expression="2 + 2", report_usage=True)
print("Result:", result)
print("CPU Time (ns):", result.get("cpu_time_ns", "N/A"))
```



### Custom Functions
Extend `OQS` capabilities by adding custom functions.

```python
from oqs import (oqs_engine, OQSInterpreter, FunctionNode)
from oqs.errors import OQSTypeError
from oqs.utils.shortcuts import get_oqs_type


def custom_multiply(interpreter: OQSInterpreter, node: FunctionNode) -> int | float:
    if not (2 < len(node.args) < 2):
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    arg_1, arg_2 = [interpreter.evaluatate(arg) for arg in node.args]
    if isinstance(arg_1, (int, float)) and isinstance(arg_2, (int, float)):
        return arg_1 * arg_2
    else:
        raise OQSTypeError(f"Cannot multiply '{get_oqs_type(arg_1)}' by '{get_oqs_type(arg_2)}'.")

    
result: dict[str, dict[str, any]] = oqs_engine(expression="custom_multiply(2, 3)", additional_functions=[("custom_multiply", custom_multiply)])
print(result)
```



### Data Types
`OQS` supports its own data types. They are as follows:
- `Number`: A parent type to the two following types:
  - `Integer`: Any value not surrounded by quotations `"` `'` that includes only digits and underscores such as `1` or `1_000`.
  - `Decimal`: Any Integer containing a Decimal Point `.` such as `1.0` or `.0` or `1.` or `1_000.0`. However, it is important to note that decimals containing an underscore after the decimal or more than one decimal will raise an error.
- `String`: Any value starting with a quotation `"` or `'` and going until that quotation appears again unless it's already in a string. For example `"This is a string"` or `This is also a single 'string''`.
- `List`: A value surrounded by square brackets separating its values using commas `,` such as `[]` or `["hi", 1]`. Lists can contain any number of values of any type including Lists. Nested lists are supported such as `[[1, 2], 3].`
- `Boolean`: The values `true` and `false`.
- `KVS` or `Key-Value Store`: A value surrounded by curly brackets and separating its keys and values using a colon `:` and separating its pairs using commas `,` and such as `{}` or `{"hi": 1, "hey": "hello"}`. KVSs can contain any number of values of any type including Lists. Its keys must be Strings. Nested KVSs are supported such as `{"kvs": {"1": 1, "2": 2}, "3": 3}.`
- `Null`: The value `null`.



### Error Types
`OQS` has advanced error reporting with the following errors:
- **Invalid Argument Quantity Error**: Raised when a function receives fewer or more arguments than expected.
- **Syntax Error**: Raised for general syntax mistakes in expressions.
- **Type Error**: Raised when an operation is performed on incompatible types.
- **Undefined Variable Error**: Raised when an expression refers to a variable that has not been defined.
- **Undefined Function Error**: Raised when an expression calls a function that does not exist.
- **Function Evaluation Error**: Raised when an error occurs within the execution of a function.
- **Division By Zero Error**: Raised when an attempt is made to divide by zero.
- **Unexpected Character Error**: Raised when an unexpected character is encountered in the expression.
- **Missing Expected Character Error**: Raised when an expected character is missing in the expression.



### Case Sensitivity in OQS
- **Function Names**: In `OQS`, function names are not case-sensitive. For example, `add`, `Add`, and `ADD` are treated as the same function. 
- **Variable Names**: Contrary to function names, variable names in `OQS` are case-sensitive. This means `var`, `Var`, and `VAR` are considered different variables.



### Using Variables
Variables in `OQS` can be used to store data that can be referred to in your expressions. They are defined as key-value pairs and passed to the `oqs_engine`. Here's an example:

```python
from oqs import oqs_engine


# Using variables in expressions
variables: dict[str, any] = {"x": 10, "y": 20}
result: dict[str, dict[str, any]] = oqs_engine(expression="x * y", variables=variables)
print(result)
```



### Nested Expressions and Evaluation
`OQS` fully supports nested expressions and evaluations anywhere within an expression, including in function calls. Here's how it works:

```python
from oqs import oqs_engine


# Nested expressions
result: dict[str, dict[str, any]] = oqs_engine(expression="ADD(1, MULTIPLY(x, y))", variables={"x": 2, "y": 3})
print(result)
```



### Unpacking in OQS
Unpacking in `OQS` is done using the `***` notation. It's used to expand lists or KVSs directly into function arguments or to create new lists/KVSs. Here's an example:

```python
from oqs import oqs_engine


# Unpacking a list into function arguments
variables: dict[str, any] = {"numbers": [1, 2, 3]}
result: dict[str, dict[str, any]] = oqs_engine(expression="SUM(***numbers)", variables=variables)
print(result)
```


### Translation to Python Types
When `OQS` evaluates an expression, the final types are translated to Python types for seamless integration. Here's how `OQS` types map to Python types:

- `Number` (both `Integer` and `Decimal`): Translated to Python's `int` or `float`. 
- `String`: Becomes Python's `str`. 
- `List`: Translated to Python's `list`. 
- `Boolean`: Becomes Python's `bool`. 
- `KVS` (Key-Value Store): Translated to Python's `dict`. 
- `Null`: Becomes Python's `None`.

- For example, an `OQS` list `[1, "hello", true]` would be translated to the Python list `[1, "hello", True]`.



## Contributing
Contributions to the `OQS` Python implementation are welcome. Please follow the guidelines in the [main `OQS` repository](https://github.com/Infuzu/OQS/tree/main) for contributing.




## License
This project is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). More details about that can be found in the [Main Repository License](https://github.com/Infuzu/OQS/blob/main/LICENSE.md).




## Authors
The `OQS` Python Implementation was built and is being maintained through the support of [Infuzu](https://infuzu.com)

Core Contributors of the `OQS` Python Implementation are as follows:
- [Yidi Sprei](https://yidisprei.com)
