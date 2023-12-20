from .errors import OQSSyntaxError
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

    @staticmethod
    def tokenize_expression(expression: str) -> list[str]:
        try:
            tokens: list[str] = []
            current_token: list[str] = []
            level: int = 0
            i: int = 0
            decimal_flag: bool = False
            while i < len(expression):
                char: str = expression[i]
                if char in ['"', "'"]:
                    if current_token:
                        tokens.append(''.join(current_token))
                        current_token: list[str] = []
                    string_char: str = char
                    current_token.append(char)
                    i += 1
                    while i < len(expression) and expression[i] != string_char:
                        current_token.append(expression[i])
                        i += 1
                    if i < len(expression):
                        current_token.append(expression[i])
                    i += 1
                elif char in ['(', '{', '[']:
                    if current_token:
                        tokens.append(''.join(current_token))
                        current_token: list[str] = []
                    level += 1
                    current_token.append(char)
                    i += 1
                elif char in [')', '}', ']']:
                    if current_token:
                        tokens.append(''.join(current_token))
                        current_token: list[str] = []
                    level -= 1
                    current_token.append(char)
                    i += 1
                    if level == 0:
                        tokens.append(''.join(current_token))
                        current_token: list[str] = []
                elif level == 0:
                    if char.isdigit() or (char == '.' and not decimal_flag):
                        if char == '.':
                            decimal_flag: bool = True
                        current_token.append(char)
                    else:
                        if current_token:
                            tokens.append(''.join(current_token))
                            current_token: list[str] = []
                            decimal_flag: bool = False
                        if char in ['+', '-', '*', '/', '%', '<', '>', '=', '!']:
                            next_char: str = expression[i + 1] if i + 1 < len(expression) else ''
                            next_next_char: str = expression[i + 2] if i + 2 < len(expression) else ''
                            if char + next_char + next_next_char in ['===', '!==']:
                                tokens.append(char + next_char + next_next_char)
                                i += 2
                            elif char + next_char in ['==', '!=', '<=', '>=', '**']:
                                tokens.append(char + next_char)
                                i += 1
                            else:
                                tokens.append(char)
                        elif char not in [',', ' ']:
                            tokens.append(char)
                    i += 1
                else:
                    current_token.append(char)
                    i += 1
            if current_token:
                tokens.append(''.join(current_token))
            tokens: list[str] = [token.strip() for token in tokens]
            print(tokens)
            return tokens
        except Exception as e:
            raise OQSSyntaxError(f"Invalid syntax: {str(e)}")

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
