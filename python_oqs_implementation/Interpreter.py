from typing import Callable
from . import built_in_functions
from .errors import (
    OQSUndefinedFunctionError, OQSBaseError, OQSFunctionEvaluationError, OQSUndefinedVariableError, OQSSyntaxError,
    OQSTypeError,
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
    ComparisonOpNode, PackedNode
)
from .parser import OQSParser


class OQSInterpreter:
    def __init__(self, parser: OQSParser) -> None:
        self.parser: OQSParser = parser
        self.variables: dict[str, any] = {}
        self.operators: dict[str, str] = {
            '+': "ADD", '-': "SUBTRACT", '*': "MULTIPLY", '/': "DIVIDE", '%': "MODULO", '**': "EXPONENTIATE"
        }
        self.functions: dict[str, Callable] = {
            "ADD": built_in_functions.bif_add,
            "SUBTRACT": built_in_functions.bif_subtract,
            "MULTIPLY": built_in_functions.bif_multiply,
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
            elements: list[any] = []
            for elem in node.elements:
                if isinstance(elem, PackedNode):
                    evaluated_elem: any = self.evaluate(self.parser.parse_expression([elem.expression], 0))
                    if isinstance(evaluated_elem, list):
                        elements.extend([self.evaluate(element) for element in evaluated_elem])
                    else:
                        raise OQSTypeError(message="Cannot unpack anything into a list construction other than a List.")
                else:
                    elements.append(self.evaluate(elem))
            return elements
        elif isinstance(node, VariableNode):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise OQSUndefinedVariableError(node.name)
        elif isinstance(node, BinaryOpNode):
            if node.op in self.operators:
                function_node: FunctionNode = FunctionNode(name=self.operators[node.op], args=[node.right, node.left])
                return self.functions[function_node.name](self, function_node)
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
                    args: list[ASTNode] = []
                    for arg in node.args:
                        if isinstance(arg, PackedNode):
                            evaluated_arg: any = self.evaluate(
                                self.parser.parse_expression([arg.expression], 0)
                            )
                            if isinstance(evaluated_arg, list):
                                args.extend(
                                    [self.parser.parse_expression([argument], pos=0) for argument in evaluated_arg]
                                )
                            else:
                                raise OQSTypeError(
                                    message="Cannot unpack anything into a function call other than a List."
                                )
                        else:
                            args.append(arg)
                    return self.functions[node.name.upper()](self, FunctionNode(name=node.name, args=args))
                else:
                    raise OQSUndefinedFunctionError(function_name=node.name)
            except OQSBaseError:
                raise
            except Exception as e:
                raise OQSFunctionEvaluationError(function_name=node.name, message=str(e))
        elif isinstance(node, KVSNode):
            kvs: dict[str, any] = {}
            for key, value in node.key_value_store.items():
                if isinstance(value, PackedNode):
                    unpacked_node: any = self.evaluate(self.parser.parse_expression([value.expression], 0))
                    if isinstance(unpacked_node, list):
                        unpacked_kvs: dict[str, any] = self.evaluate(
                            FunctionNode(name="UNPACKED_KVS", args=unpacked_node)
                        )
                        for unpacked_key, unpacked_value in unpacked_kvs.items():
                            kvs[unpacked_key] = unpacked_value
                    elif isinstance(unpacked_node, dict):
                        for unpacked_key, unpacked_value in unpacked_node.items():
                            kvs[self.evaluate(unpacked_key)] = self.evaluate(unpacked_value)
                    else:
                        raise OQSTypeError(
                            message="Cannot unpack anything into a KVS construction other than a List or KVS."
                        )
                else:
                    kvs[self.evaluate(key)] = self.evaluate(value)
            return {self.evaluate(key): self.evaluate(value) for key, value in node.key_value_store.items()}
        elif isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, UnevaluatedNode):
            return self.evaluate(self.parser.parse(node.token))
        else:
            raise OQSSyntaxError(f"Unable to parse the following: {node}")

    def set_variables(self, variable_map: dict[str, any]) -> None:
        self.variables: dict[str, any] = variable_map
