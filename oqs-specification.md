# RFC: OQS (Open Quick Script) Specification
## Abstract
This document serves as the official Request For Comments (RFC) for the Open Quick Script (OQS) language specification. The goal of OQS is to provide a generic, lightweight, and system-agnostic scripting language to be easily integrated into any platform, capable of evaluating expressions with basic types and operators. The language should accept a single expression, accompanied by an optional dictionary/map/JSON of variables, and produce a result consistent with the expression's logic.



## Introduction
OQS is designed to facilitate lightweight scripting across various systems, allowing for simple expressions involving mathematical, logical, and list operations to be evaluated in an isolated environment without any knowledge of the host system. Implementations of the language engine are free to be developed by any party, provided they adhere to the specifications outlined in this document.



## Language Specification
### Expression Input
The language engine MUST accept an input expression as a string. The expression can involve valriables, literals, and operators that will conform to the guidelines below.


### Variables Input
The engine MUST accept an optional input which is a any number of key-value pairs containing variable names with their definitions. Examples include JSON object, dictionary, or map. The input MUST NOT be mandatory. if not provided, the engine SHOULD assume there are no valraibles to substitute within the expression.


### Output Format
The engine SHOULD output results as a JSON object or map, indicating the result and any additional information regarding the evaluation (like any errors encountered).


### String-Embedded Expressions
The engine MUST accept an optional boolean input `string_embedded` that defaults to `false`. If `true`, the engine MUST treat the input expression as a string where segments enclosed in `<{` and `}>` are evaluated as expressions. Each evaluated expression MUST be replaced in situ and the modified string returned as output.


### Type System
OQS SHALL support the following basic types:
- Number (Integers and floating-point)
- Boolean
- List
- String


### Supported Operators
Operators define how different types interact with each other. The following is a specification of supported operators:

#### Numerical Operators
- `+`, `-`, `*`, `/`: For number types.

#### Comparison Operators
- `<`, `>`, `<=`, `>=`, `!=`: Operands MUST be of the same type and MUST return a Boolean value indicating the outcome of the comparison.

#### List Operators
- `+`: MUST append two lists together.
An attempt to use an unsupported operator or use an operator on imcomplete types MUST result in an error.


### Type Interactions 
OQS SHALL define explicitly how types interact with each other:

| Operator | Operand 1 | Operand 2 | Result   |
|----------|-----------|-----------|----------|
| +        | Number    | Number    | Number   |
| +        | List      | List      | List     |
| -        | Number    | Number    | Number   |
| *        | Number    | Number    | Number   |
| /        | Number    | Number    | Number   |
| <        | Number    | Number    | Boolean  |
| <=       | Number    | Number    | Boolean  |
| ==       | Any Type  | Any Type  | Boolean  |
| !=       | Any Type  | Any Type  | Boolean  |
| >        | Number    | Number    | Boolean  |
| >=       | Number    | Number    | Boolean  |

Note: "Any Type" indicatres that as long as both operands are of the same type, the comparison is valid.


### Error Handling
The language engine SHOULD return detailed errors in cases of:
- Usage of undefined variables.
- Incorrect type operations.
- Syntax errors within expressions.


### Examples
The following are non-exhaustive examples of expected inputs and outputs:
- **Input**: `{"expression": "1 + 2"}` **Output**: `{"results": 3}`
- **Input**: `{"expression": "<{variable_1 * variable_2>} is the result.", "string_embedded": true, "variables": {"variable_1": 2, "variable_2": 3}}` **Output**: `{"results": "6 is the result"}`
- **Input**: `{"expression": "variable_1 * variable_2", "variables": {"variable_1": 2, "variable_2": 3}}` **Output**: `{"results": 6}`


### Implementation Guidelines
- The specifications outlined in this RFC SHOULD be public and accessible for any potential implementer.
- Implementers SHALL comply with the type system and operator interactions as described.
- Error handling and reporting SHOULD be clear and as verbose as possible without compromising security.
- Implementations MAY be open-source or proprietary.



## Publication and Versioning
- The RFC SHOULD be published as a Markdown file (`.md`) within a GitHub repository dedicatored to the project.
- Susequent updates to the language specification should be tracked through versioning within the RFC document.
- Discussion and revision proposals SHOULD be conducted through issues and pull requests within the GitHub repository to maintain a transparent record of changes and community involvement.



## Implementation Reference
An open-source reference implementation will be made available, which follows the RFC as closely as possible and serves as a baseline for other implementations to compare against.



## Conclusion
The OQS language seeks to provide an easy-to-implement, system-agnostic scripting capability that prioritizes consistency and simplicity. Feedback and contributions to this RFC are welcomed to ensure OQS serves a wide range of use cases and remains adaptable for future needs.
