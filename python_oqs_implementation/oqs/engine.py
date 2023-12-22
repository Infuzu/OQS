import re
from .interpreter import OQSInterpreter
from .parser import OQSParser
from .nodes import ASTNode
from .errors import OQSBaseError
from .utils import get_oqs_type


def oqs_engine(
        expression: str, variables: dict[str, any] | None = None, string_embedded: bool = False
) -> dict[str, any]:
    try:
        if string_embedded:
            def replace_embedded(match: re.match):
                embedded_expr: str = match.group(1)
                embedded_result: dict[str, any] = oqs_engine(
                    expression=embedded_expr, variables=variables, string_embedded=False
                )
                return str(embedded_result["results"]["value"])

            result_expression: str = re.sub(r'<\{(.*?)\}>', replace_embedded, expression)
            return {"results": {"value": result_expression, "type": "String"}}

        result: any = OQSInterpreter(expression=expression, variables=variables).results()

        return {"results": {"value": result, "type": get_oqs_type(result)}}
    except OQSBaseError as e:
        return {"error": {"type": e.readable_name, "message": str(e)}}
    except Exception as e:
        return {
            "error": {
                "type": "unknown", "message": "An unknown error occurred. Please reach out to our help team immediately"
            },
            "additional_info": {"type": type(e).__name__, "message": str(e)}
        }
