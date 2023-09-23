def add_values_to_struct(struct, s2):
    """
    Adds values from s2 to struct, if the keys do not exist already.
    Recurses into nested dictionaries.

    :param struct: struct to add values to
    :param s2: struct to get the values from
    :return: modified version of struct
    """
    for k in s2:
        if k in struct and isinstance(struct[k], dict):
            add_values_to_struct(struct[k], s2[k])
        elif k not in struct:
            struct[k] = s2[k]

    return struct


def overwrite_existing_values_in_struct(struct, s2, check_same_type=True):
    """
    Overwrites values corresponding to shared keys in <struct> and <s2>.
    If <check_same_type>, values must be the same type to be overwritten.

    :param struct: Struct to overwrite
    :param s2: Struct with values to overwrite
    :param check_same_type: whether to check same type
    :return: modified struct
    """
    for k in s2:
        if k in struct and isinstance(struct[k], dict):
            overwrite_existing_values_in_struct(struct[k], s2[k])
        elif k in struct:
            if not check_same_type or isinstance(struct[k], type(s2[k])):
                struct[k] = s2[k]

    return struct
