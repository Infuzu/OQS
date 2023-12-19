import json
import operator
import re


OQS_TYPE_MAPPING: dict[type, str] = {
    int: 'Integer',
    float: 'Decimal',
    str: 'String',
    list: 'List',
    dict: 'KVS',
    bool: 'Boolean',
    type(None): 'Null'
}


class OQSBaseError(Exception):
    def __init__(
            self,
            readable_name: str = "OQS Base Error",
            message: str = "An error occurred while evaluating your expression!"
    ) -> None:
        super().__init__(message)
        self.readable_name: str = readable_name


class OQSInvalidArgumentQuantityError(OQSBaseError):
    def __init__(self, function_name: str, expected_min: int, expected_max: int, actual: int) -> None:
        message: str = (
            f"Function '{function_name}' expected at least {expected_min} with a max of {expected_max} arguments, "
            f"but got {actual}"
        )
        super().__init__(readable_name="Invalid Argument Quantity Error", message=message)


class OQSSyntaxError(OQSBaseError):
    def __init__(self, message: str) -> None:
        super().__init__(readable_name="Syntax Error", message=message)


class OQSTypeError(OQSBaseError):
    def __init__(self, message: str) -> None:
        super().__init__(readable_name="Type Error", message=message)


class OQSUndefinedVariableError(OQSBaseError):
    def __init__(self, variable_name: str) -> None:
        message: str = f"The variable {variable_name} is not defined."
        super().__init__(readable_name="Undefined Variable Error", message=message)


class OQSUndefinedFunctionError(OQSBaseError):
    def __init__(self, function_name: str) -> None:
        message: str = f"The function '{function_name}' is not a valid function."
        super().__init__(readable_name="Undefined Function Error", message=message)


class OQSFunctionEvaluationError(OQSBaseError):
    def __init__(self, function_name: str, message: str) -> None:
        full_message: str = f"Error in function '{function_name}': {message}"
        super().__init__(readable_name="Function Evaluation Error", message=full_message)


class ASTNode:
    pass


class NullNode(ASTNode):
    pass


class UnevaluatedNode(ASTNode):
    def __init__(self, token: str) -> None:
        self.token: str = token


class BinaryOpNode(ASTNode):
    def __init__(self, left: any, op: str, right: any) -> None:
        self.left: any = left
        self.op: str = op
        self.right: any = right


class NumberNode(ASTNode):
    def __init__(self, value: int | float) -> None:
        self.value: int | float = value


class VariableNode(ASTNode):
    def __init__(self, name: str) -> None:
        self.name: str = name


class StringNode(ASTNode):
    def __init__(self, value: str) -> None:
        self.value: str = value


class ListNode(ASTNode):
    def __init__(self, elements: list[any]) -> None:
        self.elements: list[any] = elements


class KVSNode(ASTNode):
    def __init__(self, key_value_store: dict[ASTNode, ASTNode]) -> None:
        self.key_value_store: dict[ASTNode, ASTNode] = key_value_store


class BooleanNode(ASTNode):
    def __init__(self, value: bool) -> None:
        self.value: bool = value


class FunctionNode(ASTNode):
    def __init__(self, name: str, args: list[any]) -> None:
        self.name: str = name
        self.args: list[any] = args


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
            while i < len(expression):
                char: str = expression[i]
                if char in ['"', "'"]:
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
                    level += 1
                    current_token.append(char)
                    i += 1
                elif char in [')', '}', ']']:
                    level -= 1
                    current_token.append(char)
                    i += 1
                    if level == 0:
                        tokens.append(''.join(current_token))
                        current_token: list[str] = []
                elif char == ',' and level == 0:
                    if current_token:
                        tokens.append(''.join(current_token))
                        current_token: list[str] = []
                    i += 1
                else:
                    current_token.append(char)
                    i += 1
            if current_token:
                tokens.append(''.join(current_token))
            tokens: list[str] = [token.strip() for token in tokens]
            return tokens
        except Exception as e:
            raise OQSSyntaxError(f"Invalid syntax: {str(e)}")

    def parse_expression(self, tokens: list[str], pos: int = 0) -> ASTNode | type(None):
        left: ASTNode = self.parse_term(tokens=tokens, pos=pos)
        pos += 1
        if pos < len(tokens):
            op: str = tokens[pos]
            pos += 1
            right: ASTNode = self.parse_expression(tokens, pos)
            return BinaryOpNode(left=left, op=op, right=right)
        return left

    def parse_term(self, tokens: list[str], pos: int) -> ASTNode:
        token: str = tokens[pos]
        if token.isdigit():
            return NumberNode(value=int(token))
        elif token in ['true', 'false']:
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


class OQSInterpreter:
    def __init__(self) -> None:
        self.variables: dict[str, any] = {}
        self.operators: dict[str, any] = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
        }

    def evaluate_function(self, node: FunctionNode) -> any:
        try:
            if node.name == 'ADD':
                if len(node.args) < 2:
                    raise OQSInvalidArgumentQuantityError(
                        function_name=node.name, expected_min=2, expected_max=1000000, actual=len(node.args)
                    )
                evaluated_args: list[ASTNode] = [self.evaluate(arg) for arg in node.args]
                return sum(evaluated_args)
            else:
                raise OQSUndefinedFunctionError(node.name)
        except OQSBaseError:
            raise
        except Exception as e:
            raise OQSFunctionEvaluationError(function_name=node.name, message=str(e))

    def evaluate(self, node: ASTNode) -> any:
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, NullNode):
            return None
        elif isinstance(node, ListNode):
            return [self.evaluate(elem) for elem in node.elements]
        elif isinstance(node, VariableNode):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise OQSUndefinedVariableError(node.name)
        elif isinstance(node, BinaryOpNode):
            left: any = self.evaluate(node.left)
            right: any = self.evaluate(node.right)
            return self.operators[node.op](left, right)
        elif isinstance(node, FunctionNode):
            return self.evaluate_function(node)
        elif isinstance(node, KVSNode):
            return {self.evaluate(key): self.evaluate(value) for key, value in node.key_value_store.items()}
        elif isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, UnevaluatedNode):
            return self.evaluate(OQSParser().parse_expression([node.token], 0))
        else:
            raise OQSSyntaxError(f"Unable to parse the following: {node}")

    def set_variables(self, variable_map: dict[str, any]) -> None:
        self.variables: dict[str, any] = variable_map


def oqs_engine(
        expression: str, variables: dict[str, any] | None = None, string_embedded: bool = False
) -> dict[str, any]:
    try:
        if string_embedded:
            def replace_embedded(match: re.match):
                embedded_expr: str = match.group(1)
                embedded_result: dict[str, any] = oqs_engine(
                    expression=embedded_expr, variables=variables, string_embedded=False
                )
                return str(embedded_result["results"]["value"])

            expression: str = re.sub(r'<\{(.*?)\}>', replace_embedded, expression)

        parser: OQSParser = OQSParser()
        ast: ASTNode = parser.parse(expression=expression)

        interpreter: OQSInterpreter = OQSInterpreter()
        if variables:
            interpreter.set_variables(variables)
        result: any = interpreter.evaluate(ast)

        oqs_type: str = OQS_TYPE_MAPPING.get(type(result), 'Unknown')

        return {"results": {"value": result, "type": oqs_type}}
    except OQSBaseError as e:
        return {"error": {"type": e.readable_name, "message": str(e)}}
    except Exception as e:
        return {
            "error": {
                "type": "unknown", "message": "An unknown error occurred. Please reach out to our help team immediately"
            },
            "additional_info": {"type": type(e).__name__, "message": str(e)}
        }


def main():
    expression: str = "SUB(2, 5, 6)"
    variables: dict[str, any] = {}
    string_embedded: bool = False
    result: dict[str, any] = oqs_engine(expression=expression, variables=variables, string_embedded=string_embedded)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
