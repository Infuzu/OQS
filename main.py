import json
from python_oqs_implementation.oqs.engine import oqs_engine
from python_oqs_implementation.oqs.utils.conversion import OQSJSONEncoder
from tests.cases import generate_tests_json


def main():
    generate_tests_json()
    def expression(iteration: int = 1) -> str:
        return 'PARSE_TEMPORAL("10:00:00", "Time") + DURATION(0, 1, 0, 0)'
    variables: dict[str, any] = {}
    string_embedded: bool = False
    for i in range(1):
        result: dict[str, any] = oqs_engine(
            expression=expression(i), variables=variables, string_embedded=string_embedded, report_usage=True
        )
        print(i)
        print(json.dumps(result, indent=4, cls=OQSJSONEncoder))


if __name__ == "__main__":
    main()
