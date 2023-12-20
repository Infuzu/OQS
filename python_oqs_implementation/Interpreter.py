from typing import Callable
from . import built_in_functions
from .errors import (
    OQSUndefinedFunctionError, OQSBaseError, OQSFunctionEvaluationError, OQSUndefinedVariableError, OQSSyntaxError,
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
    UnevaluatedNode,
    ComparisonOpNode
)
from .parser import OQSParser


class OQSInterpreter:
    def __init__(self) -> None:
        self.variables: dict[str, any] = {}
        self.operators: dict[str, Callable] = {
            '+': built_in_functions.bif_add,
            '-': built_in_functions.bif_subtract,
            '*': built_in_functions.bif_multiply,
            '/': built_in_functions.bif_divide,
            '%': built_in_functions.bif_modulo,
            '**': built_in_functions.bif_exponentiate
        }
        self.functions: dict[str, Callable] = {
            "ADD": built_in_functions.bif_add,
            "SUBTRACT": built_in_functions.bif_subtract,
            "MULTIPLE": built_in_functions.bif_multiply,
            "DIVIDE": built_in_functions.bif_divide,
            "EXPONENTIATE": built_in_functions.bif_exponentiate,
            "MODULO": built_in_functions.bif_modulo,
            "INTEGER": built_in_functions.bif_integer,
            "DECIMAL": built_in_functions.bif_decimal,
            "STRING": built_in_functions.bif_string,
            "LIST": built_in_functions.bif_list,
            "KVS": built_in_functions.bif_kvs,
            "BOOLEAN": built_in_functions.bif_boolean,
            "BOOL": built_in_functions.bif_boolean,
            "KEYS": built_in_functions.bif_keys,
            "VALUES": built_in_functions.bif_values,
            "UNIQUE": built_in_functions.bif_unique,
            "REVERSE": built_in_functions.bif_reverse,
            "MAX": built_in_functions.bif_max,
            "MIN": built_in_functions.bif_min,
            "SUM": built_in_functions.bif_sum,
            "LENGTH": built_in_functions.bif_length,
            "LEN": built_in_functions.bif_length,
            "APPEND": built_in_functions.bif_append,
            "UPDATE": built_in_functions.bif_update,
            "REMOVE_ITEM": built_in_functions.bif_remove_item,
            "REMOVE": built_in_functions.bif_remove,
            "ACCESS": built_in_functions.bif_access,
            "IF": built_in_functions.bif_if
        }

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
            try:
                if node.name.upper() in self.functions:
                    return self.functions[node.name.upper()](self, node)
                else:
                    raise OQSUndefinedFunctionError(function_name=node.name)
            except OQSBaseError:
                raise
            except Exception as e:
                raise OQSFunctionEvaluationError(function_name=node.name, message=str(e))
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
