default_values = {}


def value_or_default(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return default_values[key]
