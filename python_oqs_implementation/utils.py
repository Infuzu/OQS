from .constants import OQS_TYPE_MAPPING


def get_oqs_type(item: any) -> str:
    return OQS_TYPE_MAPPING.get(type(item), 'Unknown')
