# `OQS` (Open Quick Script) Language Guidelines
## Version: 0.2
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


### Parentheses in Expressions
- Parentheses `()` can be used in all expressions to separate parts of the expressions and clarify priority. This is applicable in mathematical operations, string manipulation, and other contexts where expression clarity and evaluation order are crucial.


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
Language engines are expected to provide comprehensive errors for issues such as undefined variable usage, improper type manipulation, syntax mistakes in expressions, and incorrect function usage (invalid number or type of arguments).


### Built-in Functions
`OQS` should support a set of built-in functions, with each implementation having the freedom to include additional functions. (Functions must handle invalid inputs by raising appropriate errors.)
- `ADD(argument1, argument2, ...)`: Adds numbers, concatenates strings, or merges lists. Accepts an unlimited number of arguments of the same type and performs the appropriate operation based on the type.
- `SUBTRACT(argument1, argument2)`: Performs the subtraction operation on numbers, removes instances of `argument2` from `argument1` if they are strings or lists.
- `MULTIPLY(argument1, argument2, ...)`: Multiplies numbers or repeats strings/lists. For numbers, all arguments are multiplied together. For strings/lists, the first argument is repeated a number of times equal to the product of the remaining numerical arguments.
- `DIVIDE(argument1, argument2)`: Divides the first number by the second. Raises an error if the second argument is zero.
- `EXPONENTIATE(base, exponent)`:  Raises the `base` to the power of `exponent`. Both arguments must be numbers.
- `MODULO(number1, number2)`: Calculates the remainder of division of `number1` by `number2`.
- `INTEGER(arugment)`: Returns a Decimal/String/Integer/Boolean in an Integer representation.
- `DECIMAL(argument)`: Returns an Integer/String/Decimal in a Decimal representation.
- `STRING(argument)`: Returns any single type in a String representation.
- `LIST(argument1, argument2, ...)`: Returns a List containing the provided arguments in order.
- `KVS(key1, value1, key2, value2, ..., keyN, valueN)`: Returns a kvs with all key value pairs. All keys must be strings. Raises an error if there is an odd amount of arguments.
- `BOOLEAN(argument)`/`BOOL(argument)`: Returns a truthy evaluation of the argument. `0` or `0.0` will return `false` while any other number will return `true`. Empty strings or lists such as `""`, `''`, and `[]` will return `false` while the same examples with any characters or items will return `true`.
- `KEYS(kvs)`: Returns a list of all keys in a KVS.
- `VALUES(kvs)`: Returns a list of all values in a KVS.
- `UNIQUE(list)`: Returns a list of all unique values in a list.
- `REVERSE(list)`: Returns a list in reverse order.
- `MAX(number1, number2, ..., numberN)`: Returns the maximum number among the arguments.
- `MIN(number1, number2, ..., numberN)`: Returns the minimum number among the arguments.
- `SUM(list)`: adds up all items in the list if they are of the same base type. Concatenates if all items are strings, adds numerically if all are numbers and returns the result. Raises an error for mixed types.
- `LENGTH(object)`/`LEN(object)`: Returns the count of items in a list of characters in a string, integer, or decimal.
- `APPEND(list, item)`: Appends an item of any type to the end of a list and returns the adjusted list.
- `UPDATE(kvs/list, string[key for kvs]/integer[index for list], value)`: Updates a KVS or List with a new value. In lists, it raises an error if the specified index does not exist, otherwise, changes the value at specified index (supports negative indexing). In KVS, it sets the value for the specified key regardless of the current existence of that key.
- `REMOVE_ITEM(list/kvs, item, max_occurences=unlimited)`: Removes an item from a list or kvs, with an optional third argument to specify the maximum number of occurrences to remove. If not specified, it removes all occurrences. If `max_occurrences` is set to 1, it only removes the first occurrence. It ultimately returns the adjusted list/kvs.
- `REMOVE(list/kvs, index[for list]/key[for kvs])`: Removes an item from a list/kvs by index/key (supports negative indexing) and returns the adjusted list/kvs. Raises an error if the index does not exist. Does not raise an error if a key does not exist.
- `ACCESS(list/kvs, index[for list]/key[for kvs], [optional default value for kvs access])`: Returns an item from a list/kvs by index/keu (supports negative indexing). Raises an error if the index does not exist. Returns null if the key does not exist or the default value if specified in the third argument.
- `IF(condition1, result1, ..., conditionN, resultN, [else_result])`: Takes a minimum of two arguments up to an unlimited amount. Treats all arguments as condition result pairs if an even number of arguments are passes. If an odd number of arguments are passes, all but the last are treated as condition-result pairs, with the last argument being the `else` result. Returns the result corresponding to the first true condition, or the `else` result if none are met. Conditions are evaluated for truthiness, and no condition or result is evaluated until needed, ensuring that errors in non-relevant conditions or results do not affect the evaluation.


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