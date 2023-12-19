# `OQS` (Open Quick Script) Language Guidelines
## Overview
This document establishes the comprehensive guidelines for the `OQS` (Open Quick Script) language. `OQS` aims to be a universally adoptable, streamlined, and system-neutral scripting language that integrates effortlessly into diverse platforms. It is specifically crafted to process expressions encompassing fundamental types and operations, interpreting a solitary expression—optionally accompanied by a dictionary, map, or JSON containing variables—to yield a consistent and logical outcome.



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
  - Intgers
  - Decimals
- Booleans
- Lists
- Strings
- Functions


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

#### String Operators
- Concatenation `+`: Combined two strings into one.
- Subtraction `-`: Removes all instances of the entirety of the second string from the first string.
- Repetition `*`L Repeats a string by the multiplier specified (must be a non-negative integer).

#### Function Invation
- The syntax for invoking functions is an identifier that starts with a letter followed by any combination of letters, numbers, or underscores, then an opening parenthesis `(`, an optional comma-seperated list of arguments, and a closing parentheses `)`.


### Paretheses in Expressions
- Parentheses `()` can be used in all expressions to seperate parts of the expressions and clarify priority. This is applicable in mathematical operations, string manipulation, and other contexts where expression clarity and evaluation order are crucial.


### Unpacking Syntax in Function Calls and List Creation
`OQS` includes an unpacking feature using the `*` notation. This allows for the expansion of list items directly into function arguments or for the creation of new lists.
- In function calls, such as `INTEGER(*variable_1)` where `variable_1` contains `["1"]`, it will unpack the list and pass "1" as an argument to the `INTEGER` function, effectively calling `INTEGER("1")`.
- For lists, the syntax `[*variable_1, *variable_2]` will combine the elements of `variable_1` and `variable_2` into a single list. For instance, if `variable_1 = [1, 2, 3]` and `variable_2 = [4, 5, 6]`, the result would be `[1, 2, 3, 4, 5, 6]`. This is functionally equivalent to using the `+` operator for list concatenation.


### Type Interactions 
Interactions between types are explicitly defined within `OQS` as follows:

| Operator | Operand 1 | Operand 2 | Result   |
|----------|-----------|-----------|----------|
| +        | Number    | Number    | Number   |
| +        | List      | List      | List     |
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
- `INTEGER(arugment)`: Returns a Decimal/String/Integer/Boolean in an Integer representation.
- `DECIMAL(argument)`: Returns an Integer/String/Decimal in a Decimal representation.
- `STRING(argument)`: Returns any single type in a String representation.
- `LIST(argument1, argument2, ...)`: Returns a List containing the provided arguments in order.
- `BOOLEAN(argument)`/`BOOL(argument)`: Returns a truthi evaluation of the argument. `0` or `0.0` will return `false` while any other number will return `true`. Empty strings or lists such as `""`, `''`, and `[]` will return `false` while the same examples with any characters or items will return `true`.
- `SUM(list)`: adds up all items in the list if they are of the same base type. Cancatenates if all items are strings, adds numerically if all are numbers and returns the result. Raises an error for mixed types.
- `LENGTH(object)`/`LEN(object)`: Returns the count of items in a list of characters in a string, integer, or decimal.
- `APPEND(list, item)`: Appends an item of any type to the end of a list and returns the adjusted list.
- `REMOVE_ITEM(list, item, max_occurences=unlimited)`: Removes an item from a list, with an optional third argument to specify the maximum number of occurrences to remove. If not specified, it removes all occurrences. If `max_occurrences` is set to 1, it only removes the first occurrence. It ultimately returns the adjusted list.
- `REMOVE_INDEX(list, index)`: Removes an item from a list by index (supports negative indexing) and returns the adjusted list. Raises an error if the index does not exist.
- `ACCESS_INDEX(list, index)`: Returns an item from a list by index (supports negative indexing). Raises an error if the index does not exist.
- `IF(condition1, result1, ..., conditionN, resultN, [else_result])`: Takes a minimum of two arguments up to an unlimited amount. Treats all arguments as condition result pairs if an even number of arguments are passes. If an odd number of arguments are passes, all but the last are treated as condition-result pairs, with the last argument being the `else` result. Returns the result corresponding to the first true condition, or the `else` result if none are met. Conditions are evaluated for truthiness, and no condition or result is evaluated until needed, ensuring that errors in non-relavant conditions or results do not affect the evaluation.


### Examples
#### Consistency Across Implementations:
Expressions evaluated in `OQS` should yield identical results across different implementations. This consistency is vital, except in cases where custom features or extensions have been introduced. The following are sample expressions and their expected outputs:
- **Input**: `1 + 2` **Output**: `3`
- **Input**: `variable_1 - variable_2` with variables `{"variable_1": 5, "variable_2": 2}` **Output**: `3`
- **Input**: `5 ** 2` **Output**: `25`
- **Input**: `5 % 2` **Output**: `1`
- **Input**: `[1, 2] + [3, 4]` **Output**: `[1, 2, 3, 4]`
- **Input**: `[1, 2, 3, 4] - [2, 4]` **Output**: `[1, 3]`
- **Input**: `"Hello, " + "World!"` **Output**: `"Hello, World!"`
- **Input**: `"leeee" - "e"` **Output**: `"l"`
- **Input**: `"leeee" - "le"` **Output**: `"eee"`
- **Input**: `"Loops" * 3` **Output**: `"LoopsLoopsLoops"`
- **Input**: `<{3 + 5}> is the answer` with `string_embedded` set to `true` **Output**: `"8 is the answer"`
- **Input**: `INTEGER("123")` **Output**: `123`
- **Input**: `DECIMAL(123)` **Output**: `123.0`
- **Input**: `STRING([true, 123, "test"])` **Output**: `"[true, 123, 'test']"`
- **Input**: `LIST(1, "two", 3.5)` **Output**: `[1, "two", 3.5]`
- **Input**: `[BOOL([]), BOOLEAN([]), BOOL([1]), BOOL(0), BOOL(1)]` **Output**: `[false, false, true, false, true]`
- **Input**: `INTEGER(*["123"])` **Output**: `123`
- **Input**: `SUM([1, 2, 3])` **Output**: `6`
- **Input**: `LEN("Hello")` **Output**: `5`
- **Input**: `APPEND([1, 2], 3)` **Output**: `[1, 2, 3]`
- **Input**: `REMOVE_ITEM([1, 2, 3], 2)` **Output**: `[1, 3]`
- **Input**: `REMOVE_ITEM([1, 2, 2, 3], 2, 1)` **Output**: `[1, 2, 3]`
- **Input**: `REMOVE_INDEX([1, 2, 3], 0)` **Output**: `[2, 3]`
- **Input**: `ACCESS_INDEX([1, 2, 3], -1)` **Output**: `3`
- **Input**: `IF(1 < 2, "yes", 2 < 1, "no", "maybe")` **Output**: `"yes"`
- **Input**: `IF(false, "no", "maybe")` **Output**: `"maybe"`
- **Input**: `[*[1, 2, 3], *[4, 5, 6]]` **Output**: `[1, 2, 3, 4, 5, 6]`


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
