def convert_enum_to_value(enum_value):
    if hasattr(enum_value, 'value'):
        return enum_value.value
    return enum_value