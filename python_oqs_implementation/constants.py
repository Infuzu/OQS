OQS_TYPE_MAPPING: dict[type, str] = {
    int: 'Integer',
    float: 'Decimal',
    str: 'String',
    list: 'List',
    dict: 'KVS',
    bool: 'Boolean',
    type(None): 'Null'
}
