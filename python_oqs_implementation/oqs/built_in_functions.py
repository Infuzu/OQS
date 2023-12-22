from .constants import MAX_ARGS
from .errors import (OQSInvalidArgumentQuantityError, OQSDivisionByZeroError, OQSTypeError)
from .nodes import FunctionNode
from .utils import get_oqs_type


def bif_add(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float | list | str | dict:
    if len(node.args) < 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=MAX_ARGS, actual=len(node.args)
        )
    evaluated_args: list[any] = [interpreter.evaluate(arg) for arg in node.args]
    completion: any = evaluated_args.pop(0)
    for evaluated_arg in evaluated_args:
        if isinstance(completion, (int, float)) and isinstance(evaluated_arg, (int, float)):
            completion += evaluated_arg
        elif isinstance(completion, list) and isinstance(evaluated_arg, list):
            completion += evaluated_arg
        elif isinstance(completion, str) and isinstance(evaluated_arg, str):
            completion += evaluated_arg
        elif isinstance(completion, dict) and isinstance(evaluated_arg, dict):
            for key, value in evaluated_arg.items():
                completion[key] = value
        else:
            raise OQSTypeError(message=f"Cannot add '{get_oqs_type(completion)}' and '{get_oqs_type(evaluated_arg)}'")
    return completion


def bif_subtract(interpreter: 'OQSInterpreter', node: FunctionNode) -> int | float | list | str:
    if len(node.args) != 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    a, b = [interpreter.evaluate(arg) for arg in node.args]
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a - b
    elif isinstance(a, list) and isinstance(b, list):
        return [item for item in a if item not in b]
    elif isinstance(a, str) and isinstance(b, str):
        return a.replace(b, '')
    else:
        raise OQSTypeError(message=f"Cannot subtract '{get_oqs_type(completion)}' by '{get_oqs_type(evaluated_arg)}'")


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


def bif_length(interpreter: 'OQSInterpreter', node: FunctionNode) -> int:
    if len(node.args) != 1:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=1, expected_max=1, actual=len(node.args)
        )
    value: any = interpreter.evaluate(node.args[0])
    if not isinstance(value, (str, list, dict)):
        raise OQSTypeError(message="Argument must be a string, list or KVS")
    return len(value)


def bif_append(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any]:
    if len(node.args) != 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    lst, item = [interpreter.evaluate(arg) for arg in node.args]
    if not isinstance(lst, list):
        raise OQSTypeError(message="First argument must be a list")
    lst.append(item)
    return lst


def bif_update(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any] | dict[str, any]:
    if len(node.args) != 3:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=3, expected_max=3, actual=len(node.args)
        )
    container, key_or_index, value = [interpreter.evaluate(arg) for arg in node.args]
    if isinstance(container, list):
        if not isinstance(key_or_index, int):
            raise OQSTypeError(message="Index must be an integer")
        key_or_index: int = key_or_index % len(container)
        if key_or_index < 0 or key_or_index >= len(container):
            raise IndexError("List index out of range")
        container[key_or_index] = value
    elif isinstance(container, dict):
        if not isinstance(key_or_index, str):
            raise OQSTypeError(message="Key must be a string")
        container[key_or_index] = value
    else:
        raise OQSTypeError(message="First argument must be a list or KVS")
    return container


def bif_remove_item(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any] | dict[str, any]:
    if len(node.args) < 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=3, actual=len(node.args)
        )
    container, item = [interpreter.evaluate(arg) for arg in node.args[:2]]
    max_occurrences: int = interpreter.evaluate(node.args[2]) if len(node.args) == 3 else MAX_ARGS
    if not isinstance(max_occurrences, int):
        raise OQSTypeError(message="Third argument must be an Integer")
    if isinstance(container, list):
        new_list: list[str, any] = []
        for elem in container:
            if elem == item and max_occurrences > 0:
                max_occurrences -= 1
                continue
            new_list.append(elem)
        return new_list
    elif isinstance(container, dict):
        if item in container:
            del container[item]
        return container
    else:
        raise OQSTypeError(message="First argument must be a list or KVS")


def bif_remove(interpreter: 'OQSInterpreter', node: FunctionNode) -> list[any] | dict[str, any]:
    if len(node.args) != 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=2, actual=len(node.args)
        )
    container, key_or_index = [interpreter.evaluate(arg) for arg in node.args]
    if isinstance(container, list):
        if not isinstance(key_or_index, int):
            raise OQSTypeError(message="Index must be an integer")
        if key_or_index < 0 or key_or_index >= len(container):
            raise IndexError("List index out of range")
        del container[key_or_index]
    elif isinstance(container, dict):
        if not isinstance(key_or_index, str):
            raise OQSTypeError(message="Key must be a string")
        container.pop(key_or_index, None)
    else:
        raise OQSTypeError(message="First argument must be a list or KVS")
    return container


def bif_access(interpreter: 'OQSInterpreter', node: FunctionNode):
    if len(node.args) < 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=3, actual=len(node.args)
        )
    container, key_or_index = [interpreter.evaluate(arg) for arg in node.args[:2]]
    default_value = interpreter.evaluate(node.args[2]) if len(node.args) == 3 else None
    if isinstance(container, list):
        if not isinstance(key_or_index, int):
            raise OQSTypeError(message="Index must be an integer")
        if key_or_index < 0 or key_or_index >= len(container):
            raise IndexError("List index out of range")
        return container[key_or_index]
    elif isinstance(container, dict):
        return container.get(key_or_index, default_value)
    else:
        raise OQSTypeError(message="First argument must be a list or KVS")


def bif_if(interpreter: 'OQSInterpreter', node: FunctionNode) -> any:
    if len(node.args) < 2:
        raise OQSInvalidArgumentQuantityError(
            function_name=node.name, expected_min=2, expected_max=MAX_ARGS, actual=len(node.args)
        )
    for i in range(0, len(node.args) - 1, 2):
        condition: any = interpreter.evaluate(node.args[i])
        if condition:
            return interpreter.evaluate(node.args[i + 1])
    if len(node.args) % 2 != 0:
        return interpreter.evaluate(node.args[-1])
    return None
