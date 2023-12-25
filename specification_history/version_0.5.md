# `OQS` (Open Quick Script) Language Guidelines
## Version: 0.5
## Overview
This document establishes the comprehensive guidelines for the `OQS` (Open Quick Script) language. `OQS` aims to be a universally adoptable, streamlined, and system-neutral scripting language that integrates effortlessly into diverse platforms. `OQS` is not designed to be a feature complete programming language. Rather, it is designed to be a simple, yet powerful, expression engine. It is specifically crafted to process expressions encompassing fundamental types and operations, interpreting a solitary expression—optionally accompanied by a dictionary, map, or JSON containing variables—to yield a consistent and logical outcome.



## Language Design Principles
In creating these guidelines, `OQS` has been meticulously designed to empower seamless implementation of scripting across a multitude of systems. It supports straightforward mathematical, logical, list computations, and function invocations within a contained environment, devoid of dependencies on the host system's intricacies. All developers are encouraged to build language engines in compliance with these guidelines to ensure consistency and reliability across implementations.



## Language Guidelines
### Expression Input
`OQS` engines are required to accept input expressions as strings, incorporating variables, literals, and operators in alignment with the specifications set forth herein.


### Variables Input
Engines must be capable of processing an optional input of key-value pairs that represent variable names and corresponding definitions—applicable formats include JSON objects, dictionaries, or maps. This input is not mandatory; engines should default to no variable substitutions if such input is absent.


### Output Format
An efficient `OQS` engine should produce outputs in the form of a JSON object or a map that encapsulates the result and any ancillary evaluation data, such as errors encountered during the process.


### String-Embedded Expressions
Engines are mandated to consider an optional boolean parameter `string_embedded`, which is `false` by default. If set to `true`, the engine must interpret the input expression as a string wherein segments framed by `<{` and `}>` are processed as embedded expressions. Subsequent to evaluation, the resultant expressions replace the original segments, with the modified string being returned.


### Type System
`OQS` supports a core set of types, which are essential for numerous scenarios:
- Numbers: Including the subtypes:
  - Integers: Contains any numeric value not in quotations not containing any decimals `.`.
  - Decimals: Contains any numeric value not in quotations containing a single decimal `.`. Values not containing a leading number such as `.5` are still considered valid decimals. The same goes for values ending with a decimal such as `5.`
- Booleans: Contains the values `true` and `false`.
- Lists: Any number of values surrounded by square brackets `[]` and commas seperated when containing more than 1 value. Examples include `[1, "5"]` or `[1]`. Lists can contain a mixture of types. Lists maintain their order.
- Strings: Values surrounded by double-quotes `"value"` or single-quotes `'value'`. Empty strings are valid strings as well such as `''`.
- Functions: Functions can be callable using `()` after the function name. Function names must start with an alphabetic character followed by any number of alphanumeric characters and underscores or combination thereof.
- Nulls: Contains only the value `null` to indicate nothing.
- Key-Value Stores (KVS): Enclosed in `{}`, keys are strings, values van be any type, including nested KVS. It can be empty.


### Supported Operators
Operators, which are foundational to the interaction between types, are clarified below (Using unsupported operators or misapplying operators to incomplete types must trigger an error.):

#### Numerical Operators
- Addition `+`, subtraction `-`, multiplication `*`, division `/`: To be used with number types only.
- Exponentiation `**`: Used to raise a number to the power of another number. (This is valid so long as the second value is a real number)
- Modulus `%`: Used to find the remainder of division of one number by another.

#### Comparison Operators
- Less-than `<`, greater-than `>`, less-than-or-equal-to `<=`, greater-than-or-equal-to `>=`, not-equal `!=`, equal `==`, strictly equal `===`, strictly not-equal `!==`: Comparisons require identical operand types (for `===` and `!==`) or equivalent values (for `==` and `!=`) and return a Boolean value. For `==` and `!=`, type conversions are allowed (e.g., integer `0` equals decimal `0.0`, and `"0.0"` equals `0.0`).

#### List Operators
- Concatenation `+`: Required to merge two lists.
- Subtraction `-`: Removes elements of the second list from the first one, if they are present.

#### KVS Operators
- Concatenation `+`: Required to merge two KVSs. If there are duplicate keys, it prioritizes the later declaration.

#### String Operators
- Concatenation `+`: Combined two strings into one.
- Subtraction `-`: Removes all instances of the entirety of the second string from the first string.
- Repetition `*`L Repeats a string by the multiplier specified (must be a non-negative integer).

#### Function Invocation
- The syntax for invoking functions is an identifier that starts with a letter followed by any combination of letters, numbers, or underscores, then an opening parenthesis `(`, an optional comma-seperated list of arguments, and a closing parentheses `)`.


### Order of Operations
The `OQS` language adheres to a conventional order of operations to ensure predictable and logical results in expressions. This hierarchy is particularly crucial in expressions involving multiple operators:

1. Parentheses: Expressions within parentheses are evaluated first. 
2. Exponentiation: Operations involving exponentiation are next. 
3. Multiplication and Division: These operations are performed from left to right. 
4. Addition and Subtraction: Finally, addition and subtraction are performed, also from left to right.

Failing to respect this order will lead to incorrect results and may cause errors in the execution of scripts.


### Parentheses in Expressions
- In `OQS`, parentheses `()` play a pivotal role in structuring expressions. They not only clarify the sequence in which operations are performed but also allow for overriding the default order of operations. Parentheses ensure that the enclosed expression is evaluated first, regardless of the types of operations involved.


### Unpacking Syntax
`OQS` includes an unpacking feature using the `***` notation. This allows for the expansion of list items directly into function arguments or for the creation of new lists.
- In function calls, such as `INTEGER(***variable_1)` where `variable_1` contains `["1"]`, it will unpack the list and pass `"1"` as an argument to the `INTEGER` function, effectively calling `INTEGER("1")`.
- For lists, the syntax `[***variable_1, ***variable_2]` will combine the elements of `variable_1` and `variable_2` into a single list. For instance, if `variable_1 = [1, 2, 3]` and `variable_2 = [4, 5, 6]`, the result would be `[1, 2, 3, 4, 5, 6]`. This is functionally equivalent to using the `+` operator for list concatenation.
`OQS` also includes unpacking KVS using the `***` notation. This allows for the expansion of KVS items directly into function arguments or for the creation of new KVSs.
- In all standard cases such as `LIST(***variable_1)` where `variable_1` contains `{"hello": 5}`, it will unpack the kvs and pass `"hello"` and `5` as two arguments to the `LIST` function effectively calling `LIST("hello", 5)`.
- For KVS creation, the syntax `{***kvs1, ***kvs_2}` will combine the elements of `kvs1` and `kvs2` into a single KVS. For instance is `kvs1 = {"hello": 5}` and `kvs2 = {"yello": 3}`, the result would be `{"hello": 5, "yello": 3}`. This is functionally equivalent to using the `+` operator for KVS concatenation.


### Type Interactions 
Interactions between types are explicitly defined within `OQS` as follows:

| Operator | Operand 1 | Operand 2 | Result   |
|----------|-----------|-----------|----------|
| +        | Number    | Number    | Number   |
| +        | List      | List      | List     |
| +        | KVS       | KVS       | KVS      |
| +        | String    | String    | String   |
| -        | Number    | Number    | Number   |
| -        | List      | List      | List     |
| -        | String    | String    | String   |
| *        | Number    | Number    | Number   |
| *        | String    | Integer   | String   |
| /        | Number    | Number    | Number   |
| **       | Number    | Number    | Number   |
| %        | Number    | Number    | Number   |
| <        | Number    | Number    | Boolean  |
| <=       | Number    | Number    | Boolean  |
| ==       | Any Type  | Any Type  | Boolean  |
| !=       | Any Type  | Any Type  | Boolean  |
| ===      | Any Type  | Any Type  | Boolean  |
| !==      | Any Type  | Any Type  | Boolean  |
| >        | Number    | Number    | Boolean  |
| >=       | Number    | Number    | Boolean  |

("Any Type" indicates compatibility for comparisons between operands sharing a type.)


### Error Handling
`OQS` language engines must implement comprehensive error handling to ensure robust and predictable scripting experiences. The following error types and their contexts of occurrence are detailed:

#### Error Types and Contexts
- **Invalid Argument Quantity Error**
  - Raised when a function receives fewer or more arguments than expected. 
  - Example: `ADD(1)` or `ADD(1, 2, 3, 4, 5)` if `ADD` expects two arguments. 
- **Syntax Error**
  - Raised for general syntax mistakes in expressions. 
  - Example: `{"string": variable} 5` (missing operator). 
  - **Sub-Errors**:
    - **Unexpected Character Error**
      - Raised when an unexpected character is encountered in the expression. 
      - Example: `5, 5` (unexpected `,`).
    - **Missing Expected Character Error**
      - Raised when an expected character is missing in the expression. 
      - Example: `ADD(5, 6` (missing closing parenthesis).
- **Type Error**
  - Raised when an operation is performed on incompatible types. 
  - Example: `"Hello" - 5` (string and integer). 
- **Undefined Variable Error**
  - Raised when an expression refers to a variable that has not been defined. 
  - Example: `x + 2` where `x` is undefined. 
- **Undefined Function Error**
  - Raised when an expression calls a function that does not exist. 
  - Example: `NONEXISTENT_FUNCTION(1, 2)`. 
- **Function Evaluation Error**
  - Raised when an error occurs within the execution of a function. 
- **Division By Zero Error**
  - Raised when an attempt is made to divide by zero. 
  - Example: `10 / 0`. 

#### Implementing Error Handling
- Errors must provide clear and informative messages to aid in debugging. 
- Errors should be specific to the type of issue encountered to facilitate easier identification and resolution. 
- Implementations should include error handling as part of the language engine to maintain consistency across different environments.

#### Examples of Error Handling in Action:
- **Invalid Argument Quantity**: `ADD(1)` → "Invalid Argument Quantity Error: Expected 2 arguments, but got 1."
- **Syntax Error**: `"Hello" "World"` → "Syntax Error: Missing operator between expressions."
- **Type Error**: `"Hello" - 5` → "Type Error: Cannot subtract Integer from String."
- **Undefined Variable**: `x + 2` → "Undefined Variable Error: Variable 'x' is not defined."
- **Undefined Function**: `NONEXISTENT_FUNCTION(1, 2)` → "Undefined Function Error: Function 'NONEXISTENT_FUNCTION' is not a valid function."
- **Function Evaluation**: `DIVIDE(1, 0)` inside a function → "Function Evaluation Error: Division by zero in function 'DIVIDE'."
- **Division By Zero**: `10 / 0` → "Division By Zero Error: Division by zero results in undefined."
- **Unexpected Character**: `2 * 5 @ 3` → "Unexpected Character Error: '@' is not a valid character in expressions."
- **Missing Expected Character**: `ADD(5, 6` → "Missing Expected Character Error: Expected ')'."


### Built-in Functions
`OQS` should support a set of built-in functions, with each implementation having the freedom to include additional functions. (Functions must handle invalid inputs by raising appropriate errors.)
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


### Case Sensitivity
#### Function Name Case Insensitivity
- In `OQS`, function names are case-insensitive. This means that a function can be called using any combination of uppercase and lowercase letters, and it will be interpreted as the same function. 
  - Example: `ADD(1, 2)`, `add(1, 2)`, and `AdD(1, 2)` will all be interpreted as calls to the same addition function. 
- This design choice is intended to reduce errors and confusion related to function naming conventions, thereby making the language more user-friendly.

#### Variable Name Case Sensitivity
- Unlike function names, variable names in OQS are case-sensitive. This means that variables with the same spelling but different cases will be treated as distinct. 
  - Example: `Variable`, `variable`, and `VARIABLE` are considered three separate variables. 
- Case sensitivity in variable names allows for more precise and controlled scripting, as it enables distinct naming for different variables even with similar spellings.

#### Guidelines for Developers and Users
- Developers implementing `OQS` engines and users writing scripts in `OQS` should be mindful of these case sensitivity rules.
- It is recommended to follow consistent naming conventions for clarity and maintainability. For instance, using camelCase or snake_case consistently for variable names can enhance readability.


### Examples
#### Consistency Across Implementations:
Expressions evaluated in `OQS` should yield identical results across different implementations. This consistency is vital, except in cases where custom features or extensions have been introduced. The following are sample expressions and their expected outputs:
- **Numerical Operations**:
  - **Input**: `2 * 5` **Output**: `10`
  - **Input**: `10 / 2` **Output**: `5`
  - **Input**: `9 % 2` **Output**: `1`
- **String Operations**:
  - **Input**: `"Hello " + "World"` **Output**: `Hello World"`
  - **Input**: `"repeat" * 2` **Output**: `"repeatrepeat"`
  - **Input**: `"remove" - "move"` **Output**: `"re"`
- **Boolean Operations**:
  - **Input**: `true == false` **Output**: `false`
  - **Input**: `true != false` **Output**: `true`
- **List Operations**:
  - **Input**: `[1, 2] + [3, 4]` **Output**: `[1, 2, 3, 4]`
  - **Input**: `[1, 2, 3, 4] - [3]` **Output**: `[1, 2, 4]`
- **Key-Value Store Operations:**:
  - **Input**: `{ "a": 1, "b": 2 } + { "c": 3 }` **Output**: `{ "a": 1, "b": 2, "c": 3 }`
  - **Input**: `{ "name": "OQS", "type": "script" } + { "type": "language" }` **Output**: `{ "name": "OQS", "type": "language" }`
- **Function Examples**:
  - **Input**: `ADD(1, 2)` **Output**: `3`
  - **Input**: `SUBTRACT(5, 2)` **Output**: `3`
  - **Input**: `MULTIPLY(3, 4)` **Output**: `12`
  - **Input**: `DIVIDE(8, 4)` **Output**: `2`
  - **Input**: `EXPONENTIATE(2, 3)` **Output**: `8`
  - **Input**: `MODULO(5, 3)` **Output**: `2`
- **Complex Function Calls and Expressions**:
  - **Input**: `INTEGER(3.5)` **Output**: `3`
  - **Input**: `DECIMAL("42")` **Output**: `42.0`
  - **Input**: `STRING([1, 2, 3])` **Output**: `"[1, 2, 3]"`
  - **Input**: `LIST("a", "b", "c")` **Output**: `["a", "b", "c"]`
  - **Input**: `KVS("key1", "value1", "key2", "value2")` **Output**: `{ "key1": "value1", "key2": "value2" }`
  - **Input**: `BOOLEAN(1)` **Output**: `true`
  - **Input**: `KEYS({ "name": "OQS", "type": "script" })` **Output**: `["name", "type"]`
  - **Input**: `VALUES({ "name": "OQS", "type": "script" })` **Output**: `["OQS", "script"]`
  - **Input**: `UNIQUE([1, 1, 2, 2, 3])` **Output**: `[1, 2, 3]`
  - **Input**: `REVERSE([1, 2, 3])` **Output**: `[3, 2, 1]`
  - **Input**: `MAX(1, 3, 2)` **Output**: `3`
  - **Input**: `MIN(1, 3, 2)` **Output**: `1`
  - **Input**: `SUM([1, 2, 3])` **Output**: `6`
  - **Input**: `LEN("Hello")` **Output**: `5`
  - **Input**: `APPEND([1, 2], 3)` **Output**: `[1, 2, 3]`
  - **Input**: `UPDATE([1, 2, 3], 1, 4)` **Output**: `[1, 4, 3]`
  - **Input**: `REMOVE_ITEM([1, 2, 3, 2], 2)` **Output**: `[1, 3]`
  - **Input**: `REMOVE([1, 2, 3], 0)` **Output**: `[2, 3]`
  - **Input**: `ACCESS([1, 2, 3], 1)` **Output**: `2`
  - **Input**: `IF(1 > 0, "positive", "negative")` **Output**: `"positive"`
- **Unpacking and KVS Expansion**:
  - **Input**: `INTEGER(**["5"])` **Output**: `5`
  - **Input**: `{***{"key1": "value1"}, ***{"key2": "value2"}}` **Output**: `{ "key1": "value1", "key2": "value2" }`
- **String Embedded Expressions**:
  - **Input**: `<{3 + 5}> is the answer` with `string_embedded` set to `true` **Output**: `"8 is the answer"`
- **Complex Nested Expressions**:
  - **Input**: `IF(LEN("test") == 4, "valid", "invalid")` **Output**: `"valid"`
  - **Input**: `ADD(*[1, 2, 3, 4])` **Output**: `10`
  - **Input**: `MULTIPLY(STRING(2), 3)` **Output**: `"222"`
- **Order of Operations**:
  - **Input**: 2 + 3 * 4 **Output**: 14 (Multiplication is performed before addition)
  - **Input**: (2 + 3) * 4 **Output**: 20 (Parentheses alter the order, causing addition to be performed first)
- **Parentheses**:
  - **Input**: 4 * (2 + 3) **Output**: 20 (Parentheses cause addition to be prioritized over multiplication)
  - **Input**: ((2 + 3) * 4) / 2 **Output**: 10 (Nested parentheses guide the sequence of operations)



### Implementation Recommendations
- Accessibility of these guidelines is paramount for developers, hence they should be publicly available.
- Adherence to the stipulated type system and operator interactions is obligatory for implementers.
- Error reporting ought to be as transparent and informative as possible without introducing security risks.
- While implementations may be proprietary, open-source contributions are highly encouraged.



## Publication and Evolution
- The recommended format for these guidelines is a Markdown (.md) file within a committed GitHub repository for the project.
- Language development should be recorded through systematic versioning of this document.
- Community discourse and proposals for alterations are advised to take place via GitHub issues and pull requests to ensure an open and structured record of evolution.



## Reference Implementation
A model open-source implementation exemplifying these guidelines will be published to offer a standard for comparison and adherence for alternative implementations.



## Conclusion
The `OQS` language is designed to enhance ease of adoption, establish a system-neutral scripting solution, and ensure uniformity and straightforwardness. Your contributions and feedback on these guidelines are warmly welcomed to guarantee that `OQS` can adequately satisfy a broad spectrum of applications and remain adaptable for impending developments.