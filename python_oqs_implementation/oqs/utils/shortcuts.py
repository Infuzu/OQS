from ..constants.values import OQS_TYPE_MAPPING
from ..constants.types import ValueTypeStrings as VTS


def get_oqs_type(item: any) -> str:
    return OQS_TYPE_MAPPING.get(type(item), VTS.UNKNOWN)


def get_oqs_type_hierarchy(item: any) -> list[str]:
    return OQS_TYPE_MAPPING.get(type(item), [VTS.UNKNOWN])


def is_oqs_instance(item: any, oqs_type: str) -> bool:
    return oqs_type in get_oqs_type_hierarchy(item)
