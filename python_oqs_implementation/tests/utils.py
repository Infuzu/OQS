import inspect


def get_test_function_name() -> str:
    stack: list = inspect.stack()
    for frame in stack[1:]:
        if frame.function.startswith('test_'):
            return str(frame.function)
