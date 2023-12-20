import operator
from .errors import (
    OQSInvalidArgumentQuantityError,
    OQSUndefinedFunctionError,
    OQSBaseError,
    OQSFunctionEvaluationError,
    OQSUndefinedVariableError,
    OQSSyntaxError
)
from .nodes import (
    FunctionNode,
    ASTNode,
    NumberNode,
    StringNode,
    NullNode,
    ListNode,
    VariableNode,
    BinaryOpNode,
    KVSNode,
    BooleanNode,
    UnevaluatedNode, ComparisonOpNode
)
from .parser import OQSParser


class OQSInterpreter:
    def __init__(self) -> None:
        self.variables: dict[str, any] = {}
        self.operators: dict[str, any] = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '**': operator.pow
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
            if node.op in self.operators:
                return self.operators[node.op](left, right)
            else:
                raise OQSSyntaxError(f"Invalid binary operator '{node.op}'")
        elif isinstance(node, ComparisonOpNode):
            left: any = self.evaluate(node.left)
            right: any = self.evaluate(node.right)

            if node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>':
                return left > right
            elif node.op == '>=':
                return left >= right
            elif node.op == '===':
                return type(left) == type(right) and left == right
            elif node.op == '!==':
                return type(left) != type(right) or left != right
            else:
                raise OQSSyntaxError(f"Invalid comparison operator '{node.op}'")
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
