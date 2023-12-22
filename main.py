import json
from python_oqs_implementation.engine import oqs_engine


def main():
    expression: str = 'ADd(length([5, 10, ***[4, 3, "HEllo:,"]]), 20)'
    variables: dict[str, any] = {}
    string_embedded: bool = False
    result: dict[str, any] = oqs_engine(expression=expression, variables=variables, string_embedded=string_embedded)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
