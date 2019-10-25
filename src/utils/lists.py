def get_first_or_def(lst, default=None):
    return get_num_or_def(lst, default)


def get_num_or_def(lst, default=None, number=0):
    if len(lst) > number:
        return lst[number]
    else:
        return default
