class NUMBER2(object):

    def __init__(self, length, precision):
        self._length = length
        self._precision = precision

    def __call__(self, value):
        try:
            if not self._length or self._precision == 0:
                return int(value)
            return round(float(value), self._precision)
        except ValueError:
            return Exception("Value type error got {} want {}".format(value, 'int or float'))


class VARCHAR2(object):

    def __init__(self, length):
        self._length = length

    def __call__(self, value):
        if isinstance(value, str):
            if len(value) > self._length:
                raise Exception("The length of {} is too long".format(value))
            return repr((value))
        if isinstance(value, (int, float)):
            return repr((value))


class TEXT(object):

    def __call__(self, value):
        return repr(value)
