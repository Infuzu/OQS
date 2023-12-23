from ..constants.values import OQS_TYPE_MAPPING
from ..constants.types import ValueTypeStrings as VTS


def get_oqs_type(item: any) -> str:
    return OQS_TYPE_MAPPING.get(type(item), VTS.UNKNOWN)
