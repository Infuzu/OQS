import json
from python_oqs_implementation.oqs.engine import oqs_engine
from tests.cases import generate_tests_json


def main():
    generate_tests_json()
    expression: str = 'IF("text" - "t" == "ex", "Correct", "Incorrect")'
    variables: dict[str, any] = {}
    string_embedded: bool = False
    result: dict[str, any] = oqs_engine(expression=expression, variables=variables, string_embedded=string_embedded)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
