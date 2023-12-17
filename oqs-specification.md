# RFC: OQS (Open Quick Script) Specification
## Abstract
This document outlines the proposed design and functionality for Open Quick Script (OQS), a new scripting language developed with the intention to be system-agnostic, allowing for consistent execution across different platforms, provided that the executing environment adheres to the guidelines and standards set forth by this RFC.


## Introduction
OQS aims to provide a simple, expression-based scripting language that relies on passing a single expression and a dictionary/map/JSON object of variables for evaluation and execution, returning the result of the operation. The language will support basic arithmetic, comparison operators, and data types including lists. The goal is also to allow for easy extensibility while maintaining a core specification that any implementation must follow to ensure compatibility.


## Language Specification
### Basic Types
1. **Numbers**: Integers and floating-point numbers
2. **Booleans**: `true` or  `false`
3. **Strings**: A sequence of characters
4. **Lists**: An ordered collection of items

### Operators
1. **Arithmetic**: `+`, `-`, `*`, `/`
2. **Comparison**: `<`, `>`, `<=`, `>=`, `!=` (These return boolean values.)
3. **List**: `+` (concaternation of two lists)

### Variables and Expressions
1. **Variables**: A variable name must start with a letter or underscore, followed by letters, digits, or underscores.
2. **Expressions**: A syntax for combining variables, literals, and operators to produce a value.

### Evaluation
1. **Single Expression**: The language engine evaluates a single expression per execution.
2. **Variable Resolution**: Variables used in expressions are resolved using the provided dictionary/map/JSON object.
3. **Return Value**: The resulting value from the execution is returned to the caller.


## Implementation Guidelines
1. **Engine**: Any implentation engine must provide consistent results foir the same expression and input data across all platforms.
2. **Extensibility**: Implementations may introduce additional features beyond the core specification but must still adhere to the core functionality to maintain interoperability.
3. **Error Handlind**: Clear guidelines for error conditions, such as undefined variables and type errors, must be established and followed.


## Compatibility and Versioning
1. **Backward Compatibility**: Every effort must be made to avoid breaking changes. When they are unavoidable, a clear upgrade path must be provided.
2. **Versioning**: The Language will follow semantic versioning.


## Governance
The OQS project will maintain an open governance model with the following components:
1. **Core Team**: A group of maintainers who guide the development and curation of the RFC and its implementations.
2. **Contributors**: Anyone can contribute to the project by submitting requests, enhancements, or bug fixes.

## Documentation
The official documentation covering details of the core language specification, implementation guidelines, and basic usage examples will be provided alongside the RFC.

## Implementation Reference
An open-source reference implementation will be made available, which follows the RFC as closely as possible and serves as a baseline for other implementations to compare against.
