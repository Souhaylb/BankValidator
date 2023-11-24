def isNumber(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def indexOf(value, tab):
    if isNumber(value):
        return float(value)
    else:
        try:
            return tab.index(value)
        except ValueError:
            return value

