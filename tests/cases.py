import inspect
import json
from typing import Callable
from unittest import TestCase
from python_oqs_implementation.oqs.utils.conversion import OQSJSONEncoder
from python_oqs_implementation.tests.test_end_to_end import (
    TestLanguageEngineAdvanced, TestLanguageEngine, TestOQSFunctions
)


def generate_tests_json() -> None:
    def generate_test_json(test_class: Callable) -> dict[str, any]:
        test_data: dict[str, any] = {}
        test_instance: TestCase = test_class()
        test_instance.setUp()
        for method_name, method in inspect.getmembers(test_class, inspect.isfunction):
            if method_name.startswith("test_"):
                try:
                    method(test_instance)
                except AssertionError:
                    pass
                test_data[method_name] = test_instance.cases.get(method_name, [])
        return test_data

    test_classes_data: dict[str, any] = {
        "TestLanguageEngineAdvanced": generate_test_json(TestLanguageEngineAdvanced),
        "TestLanguageEngine": generate_test_json(TestLanguageEngine),
        "TestOQSFunctions": generate_test_json(TestOQSFunctions)
    }

    with open("tests.json", "w") as file:
        json.dump(test_classes_data, file, indent=4, cls=OQSJSONEncoder)
