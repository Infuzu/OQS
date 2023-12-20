import operator
from .constants import MAX_ARGS
from .errors import (OQSInvalidArgumentQuantityError, OQSDivisionByZeroError, OQSTypeError)
from .nodes import (FunctionNode, ASTNode)


def bif_add(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float:
    if len(node.args) < 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=MAX_ARGS, actual=len(node.args)
        )
    evaluated_args: list[ASTNode] = [interpreter.evaluate(arg) for arg in node.args]
    return sum(evaluated_args)


def bif_subtract(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float:
    if len(node.args) != 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    a, b = [interpreter.evaluate(arg) for arg in node.args]
    return operator.sub(a, b)


def bif_multiply(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float:
    if len(node.args) < 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=MAX_ARGS, actual=len(node.args)
        )
    result: int = 1
    for arg in node.args:
        result *= interpreter.evaluate(arg)
    return result


def bif_divide(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float:
    if len(node.args) != 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    a, b = [interpreter.evaluate(arg) for arg in node.args]
    if b == 0:
        raise OQSDivisionByZeroError()
    return a / b


def bif_exponentiate(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float | complex:
    if len(node.args) != 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    base, exponent = [interpreter.evaluate(arg) for arg in node.args]
    return pow(base, exponent)


def bif_modulo(interpreter: 'OQSInterpreter', node: FunctionNode) -> int:
    if len(node.args) != 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    a, b = [interpreter.evaluate(arg) for arg in node.args]
    return a % b


def bif_integer(interpreter: 'OQSInterpreter', node: FunctionNode) -> int:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    value: any = interpreter.evaluate(node.args[0])
    return int(value)


def bif_decimal(interpreter: 'OQSInterpreter', node: FunctionNode) -> float:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    value: any = interpreter.evaluate(node.args[0])
    return float(value)


def bif_string(interpreter: 'OQSInterpreter', node: FunctionNode) -> str:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    value: any = interpreter.evaluate(node.args[0])
    return str(value)


def bif_list(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any]:
    return [interpreter.evaluate(arg) for arg in node.args]


def bif_kvs(interpreter: 'OQSInterpreter', node: FunctionNode) -> dict[str, any]:
    if len(node.args) % 2 != 0:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=MAX_ARGS, actual=len(node.args)
        )
    kvs: dict[str, any] = {}
    for i in range(0, len(node.args), 2):
        key: any = interpreter.evaluate(node.args[i])
        if not isinstance(key, str):
            raise OQSTypeError(message='Key must be a string')
        value: any = interpreter.evaluate(node.args[i + 1])
        kvs[key] = value
    return kvs


def bif_boolean(interpreter: 'OQSInterpreter', node: FunctionNode) -> bool:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    value: any = interpreter.evaluate(node.args[0])
    return bool(value)


def bif_keys(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[str]:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    kvs: any = interpreter.evaluate(node.args[0])
    if not isinstance(kvs, dict):
        raise OQSTypeError(message='Argument must be a KVS')
    return list(kvs.keys())


def bif_values(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any]:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    kvs: any = interpreter.evaluate(node.args[0])
    if not isinstance(kvs, dict):
        raise OQSTypeError(message='Argument must be a KVS')
    return list(kvs.values())


def bif_unique(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any]:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    lst: any = interpreter.evaluate(node.args[0])
    if not isinstance(lst, list):
        raise OQSTypeError(message='Argument must be a list')
    return list(set(lst))


def bif_reverse(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any]:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    lst: any = interpreter.evaluate(node.args[0])
    if not isinstance(lst, list):
        raise OQSTypeError(message='Argument must be a list')
    return lst[::-1]


def bif_max(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float:
    if len(node.args) < 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=MAX_ARGS, actual=len(node.args)
        )
    numbers: list[any] = [interpreter.evaluate(arg) for arg in node.args]
    return max(numbers)


def bif_min(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float:
    if len(node.args) < 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=MAX_ARGS, actual=len(node.args)
        )
    numbers: list[any] = [interpreter.evaluate(arg) for arg in node.args]
    return min(numbers)


def bif_sum(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    lst: any = interpreter.evaluate(node.args[0])
    if not isinstance(lst, list) or not all(isinstance(item, (int, float)) for item in lst):
        raise OQSTypeError(message='Argument must be a list of numbers')
    return sum(lst)


def bif_length(interpreter: 'OQSInterpreter', node: FunctionNode):
    pass


def bif_append(interpreter: 'OQSInterpreter', node: FunctionNode):
    pass


def bif_update(interpreter: 'OQSInterpreter', node: FunctionNode):
    pass


def bif_remove_item(interpreter: 'OQSInterpreter', node: FunctionNode):
    pass


def bif_remove(interpreter: 'OQSInterpreter', node: FunctionNode):
    pass


def bif_access(interpreter: 'OQSInterpreter', node: FunctionNode):
    pass


def bif_if(interpreter: 'OQSInterpreter', node: FunctionNode):
    pass
