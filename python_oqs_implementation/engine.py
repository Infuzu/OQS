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


class InvalidArgumentQuantity(OQSBaseError):
    def __init__(self, function_name: str, expected_min: int, expected_max: int, actual: int) -> None:
        message: str = (
            f"Function '{function_name}' expected at least {expected_min} with a max of {expected_max} arguments, "
            f"but got {actual}"
        )
        super().__init__(readable_name="Invalid Argument Quantity", message=message)


class ASTNode:
    pass


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
    def __init__(self, key_value_store: dict[str, any]) -> None:
        self.key_value_store: dict[str, any] = key_value_store


class BooleanNode(ASTNode):
    def __init__(self, value: bool) -> None:
        self.value: bool = value


class FunctionNode(ASTNode):
    def __init__(self, name: str, args: list[any]) -> None:
        self.name: str = name
        self.args: list[any] = args


class OQSParser:
    def parse(self, expression: str) -> ASTNode:
        tokens: list[str] = re.findall(r'\b\w+\([^()]*\((?:[^\(\)]|(?R))*\)[^()]*\)|"[^"]*"|\S+', expression)
        return self.parse_expression(tokens=tokens)

    def parse_expression(self, tokens: list[str], pos: int = 0) -> ASTNode:
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
        elif token.startswith('"') and token.endswith('"') or token.startswith("'") and token.endswith("'"):
            return StringNode(value=token[1:-1])
        elif token.startswith('{') and token.endswith('}'):
            kvs: dict[str, ASTNode] = self.parse_kvs(token[1:-1])
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
        args_tokens = self.tokenize_arguments(args_str)
        args = [self.parse_expression([arg], 0) for arg in args_tokens]
        return FunctionNode(name=function_name, args=args)

    def parse_list(self, args_str: str) -> list[ASTNode]:
        if not args_str.strip():
            return []
        args_tokens: list[str] = self.tokenize_arguments(args_str=args_str)
        return [self.parse_expression(tokens=[token], pos=0) for token in args_tokens]

    def parse_kvs(self, kvs_str: str) -> dict[str, ASTNode]:
        kvs_tokens: list[str] = self.tokenize_arguments(kvs_str)
        kvs: dict[str, ASTNode] = {}

        for token in kvs_tokens:
            if ':' not in token:
                raise ValueError(f"Invalid key-value pair: {token}")
            key, value = token.split(':', 1)
            key: str = key.strip()
            value: str = value.strip()
            kvs[key] = self.parse_expression([value], 0)

        return kvs

    @staticmethod
    def tokenize_arguments(args_str: str) -> list[str]:
        tokens = []
        current_token = []
        level = 0
        i = 0
        in_string = False
        string_char = ''

        while i < len(args_str):
            char = args_str[i]

            if char in ['"', "'"]:
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                current_token.append(char)

            elif not in_string:
                if char == ',' and level == 0:
                    tokens.append(''.join(current_token).strip())
                    current_token = []
                else:
                    if char in ['(', '[', '{']:
                        level += 1
                    elif char in [')', ']', '}']:
                        level -= 1
                    current_token.append(char)
            else:
                current_token.append(char)

            i += 1

        if current_token:
            tokens.append(''.join(current_token).strip())

        return tokens


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
        if node.name == 'ADD':
            print(node.args)
            print(node.args[0].name)
            if len(node.args) < 2:
                raise InvalidArgumentQuantity(
                    function_name=node.name, expected_min=2, expected_max=1000000, actual=len(node.args)
                )
            return sum([self.evaluate(arg) for arg in node.args])
        else:
            raise ValueError("Unknown Function")

    def evaluate(self, node: ASTNode) -> any:
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, ListNode):
            return [self.evaluate(elem) for elem in node.elements]
        elif isinstance(node, VariableNode):
            return self.variables.get(node.name, None)
        elif isinstance(node, BinaryOpNode):
            left: any = self.evaluate(node.left)
            right: any = self.evaluate(node.right)
            return self.operators[node.op](left, right)
        elif isinstance(node, FunctionNode):
            return self.evaluate_function(node)
        elif isinstance(node, KVSNode):
            return {key: self.evaluate(value) for key, value in node.key_value_store}
        elif isinstance(node, BooleanNode):
            return node.value
        else:
            raise ValueError("Unknown node")

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
    expression: str = "ADD(ADD(3, 5), 2)"
    variables: dict[str, any] = {}
    string_embedded: bool = False
    result: dict[str, any] = oqs_engine(expression=expression, variables=variables, string_embedded=string_embedded)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
