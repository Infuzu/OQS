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
OPS_TYPE_HIERARCHY_MAPPING: dict[type, list[str]] = {
    int: [VTS.INTEGER, VTS.NUMBER],
    float: [VTS.DECIMAL, VTS.NUMBER],
    str: [VTS.STRING],
    list: [VTS.LIST],
    dict: [VTS.KVS],
    bool: [VTS.BOOLEAN],
    type(None): [VTS.NULL]
}


MAX_ARGS: int = 999_999_999_999
