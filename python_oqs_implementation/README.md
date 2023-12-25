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
`OQS` supports the following built-in functions:
- `ADD(argument1, argument2, ...)` - Adds Numbers, concatenates Strings, merges Lists or merges KVSs:
  - **Inputs**:
    - **Amount**: A minimum of two inputs with no maximum.
    - **Types**: All input types must be of the same type being one of the following:
      - `Number`
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
- `BOOLEAN(argument)`/`BOOL(argument)` - Evaluates the truthiness of an argument:
  - **Inputs**:
    - **Amount**: Exactly one input.
    - **Types**: Any single type.
  - **Outputs**: `Boolean`.
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
    - **Types**: All inputs must be `Number`.
  - **Outputs**: `Number`.
- `MIN(number1, number2, ..., numberN)` - Finds the minimum number:
  - **Inputs**:
    - **Amount**: A minimum of two inputs with no maximum.
    - **Types**: All inputs must be `Number`.
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
    if 2 < len(node.args) < 2:
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
