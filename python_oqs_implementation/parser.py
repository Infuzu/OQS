from .errors import (OQSSyntaxError, OQSMissingExpectedCharacterError, OQSUnexpectedCharacterError, OQSBaseError)
from .nodes import (
    ASTNode,
    BinaryOpNode,
    NumberNode,
    BooleanNode,
    NullNode,
    StringNode,
    KVSNode,
    ListNode,
    VariableNode,
    FunctionNode,
    UnevaluatedNode,
    ComparisonOpNode
)


class OQSParser:
    def parse(self, expression: str) -> ASTNode:
        tokens: list[str] = self.tokenize_expression(expression=expression)
        return self.parse_expression(tokens=tokens)

    def tokenize_expression(self, expression: str, separate_arguments: bool = False) -> list[str]:
        tokens: list[str] = []
        expression: str = expression.strip()
        level: int = 0
        start_index: int = 0
        in_quote: bool = False
        quote_char: str = ''

        if separate_arguments:
            for i, char in enumerate(expression):
                if char in ['"', "'"]:
                    if in_quote and char == quote_char:
                        in_quote: bool = False
                    elif not in_quote:
                        in_quote: bool = True
                        quote_char: str = char
                elif char in ['(', '{', '[']:
                    if not in_quote:
                        level += 1
                elif char in [')', '}', ']']:
                    if not in_quote:
                        level -= 1
                elif char == ',' and level == 0 and not in_quote:
                    tokens.append(expression[start_index:i].strip())
                    start_index: int = i + 1
            tokens.append(expression[start_index:].strip())
        else:
            i: int = 0
            while i < len(expression):
                char: str = expression[i]
                if char in ['"', "'"]:
                    # String handling
                    start_index = i
                    i += 1
                    while i < len(expression) and expression[i] != char:
                        i += 1
                    i += 1
                    tokens.append(expression[start_index:i])

                elif char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
                    # Decimal and integer handling
                    start_index = i if char != '.' else i - 1  # Include preceding 0 for decimals like .5
                    i += 1
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        i += 1
                    tokens.append(expression[start_index:i])

                elif char.isalpha() or char == '_':
                    # Variable and function handling
                    start_index = i
                    i += 1
                    while i < len(expression) and (expression[i].isalnum() or expression[i] == '_'):
                        i += 1
                    tokens.append(expression[start_index:i])

                elif char in ['+', '-', '*', '/', '%', '<', '>', '=', '!', ',']:
                    # Operator handling
                    start_index = i
                    while i + 1 < len(expression) and expression[i + 1] == char:
                        i += 1
                    i += 1
                    tokens.append(expression[start_index:i])

                elif char in ['(', '[', '{']:
                    # Nested structures handling
                    closing_char = ')' if char == '(' else ']' if char == '[' else '}'
                    level = 1
                    start_index = i
                    i += 1
                    while i < len(expression) and level > 0:
                        if expression[i] == char:
                            level += 1
                        elif expression[i] == closing_char:
                            level -= 1
                        i += 1
                    if level != 0:
                        raise OQSSyntaxError(f"Unmatched '{char}' in expression")
                    tokens.append(expression[start_index:i])

                elif char == '*' and i + 2 < len(expression) and expression[i:i + 3] == '***':
                    # Unpacking operator handling
                    tokens.append('***')
                    i += 3

                else:
                    i += 1

        return [token.strip() for token in tokens if token.strip()]

    @staticmethod
    def find_closing(expression: str, start_index: int) -> int:
        open_char: str = expression[start_index]
        closing_char: str = ')' if open_char == '(' else ']' if open_char == '[' else '}'
        level: int = 1
        i: int = start_index + 1
        while i < len(expression) and level > 0:
            if expression[i] == open_char:
                level += 1
            elif expression[i] == closing_char:
                level -= 1
            i += 1
        if level != 0:
            raise OQSSyntaxError(f"Unmatched '{open_char}' in expression")
        return i

    def parse_expression(self, tokens: list[str], pos: int = 0) -> ASTNode | type(None):
        left: ASTNode = self.parse_term(tokens=tokens, pos=pos)
        pos += 1
        while pos < len(tokens):
            op: str = tokens[pos]
            if op in ['==', '!=', '<', '<=', '>', '>=', '===', '!==']:
                pos += 1
                if pos < len(tokens):
                    right: ASTNode = self.parse_term(tokens, pos)
                    left: ASTNode = ComparisonOpNode(left=left, op=op, right=right)
                    pos += 1
                else:
                    raise OQSSyntaxError("Unexpected end of expression after comparison operator.")
            elif op in ['+', '-', '*', '/', '%', '**']:
                pos += 1
                if pos < len(tokens):
                    right: ASTNode = self.parse_term(tokens, pos)
                    left: ASTNode = BinaryOpNode(left=left, op=op, right=right)
                    pos += 1
                else:
                    raise OQSSyntaxError("Unexpected end of expression after binary operator.")
            else:
                raise OQSSyntaxError(f"Unexpected token: '{op}'")

        return left

    def parse_term(self, tokens: list[str], pos: int) -> ASTNode:
        token: str = tokens[pos]
        try:
            return NumberNode(value=int(token))
        except ValueError:
            try:
                return NumberNode(value=float(token))
            except ValueError:
                pass
        if token in ['true', 'false']:
            return BooleanNode(value=token == 'true')
        elif token == 'null':
            return NullNode()
        elif token.startswith('"') and token.endswith('"') or token.startswith("'") and token.endswith("'"):
            return StringNode(value=token[1:-1])
        elif token.startswith('{') and token.endswith('}'):
            kvs: dict[ASTNode, ASTNode] = self.parse_kvs(token[1:-1])
            return KVSNode(key_value_store=kvs)
        elif token.startswith('[') and token.endswith(']'):
            elements: list[ASTNode] = self.parse_list(args_str=token[1:-1])
            return ListNode(elements=elements)
        elif '(' in token and token.endswith(')'):
            return self.parse_function_call(token)
        else:
            return VariableNode(name=token)

    def parse_function_call(self, token: str) -> FunctionNode:
        function_name, args_str = token[:-1].split('(', 1)
        args_tokens: list[str] = self.tokenize_expression(expression=args_str)
        args: list[ASTNode] = [UnevaluatedNode(token=arg) for arg in args_tokens]
        return FunctionNode(name=function_name, args=args)

    def parse_list(self, args_str: str) -> list[ASTNode]:
        if not args_str.strip():
            return []
        args_tokens: list[str] = self.tokenize_expression(expression=args_str)
        return [self.parse_expression(tokens=[token], pos=0) for token in args_tokens]

    def parse_kvs(self, kvs_str: str) -> dict[ASTNode, ASTNode]:
        kvs_tokens: list[str] = self.tokenize_expression(expression=kvs_str)
        kvs: dict[ASTNode, ASTNode] = {}

        for token in kvs_tokens:
            key, value = self.split_key_value_pair(token)
            kvs[self.parse_expression([key], 0)] = self.parse_expression([value], 0)

        return kvs

    @staticmethod
    def split_key_value_pair(token: str) -> tuple[str, str]:
        colon_index: int = -1
        level: int = 0
        in_string: bool = False
        string_char: str = ''

        for i, char in enumerate(token):
            if char in ['"', "'"]:
                if in_string and char == string_char:
                    in_string: bool = False
                elif not in_string:
                    in_string: bool = True
                    string_char: str = char
            elif char == ":" and level == 0 and not in_string:
                colon_index: int = i
                break
            elif char in ['{', '[', '(']:
                level += 1
            elif char in ['}', '[', ')']:
                level -= 1

        if colon_index == -1:
            raise OQSSyntaxError(F"Invalid KVS pair {token}")

        key: str = token[:colon_index].strip()
        value: str = token[colon_index + 1:].strip()

        return key, value
