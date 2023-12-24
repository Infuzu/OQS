from .types import ValueTypeStrings as VTS


OQS_TYPE_MAPPING: dict[type, str] = {
    int: VTS.INTEGER,
    float: VTS.DECIMAL,
    str: VTS.STRING,
    list: VTS.LIST,
    dict: VTS.KVS,
    bool: VTS.BOOLEAN,
    type(None): VTS.NULL
}


MAX_ARGS: int = 999_999_999_999
