
class ListUtil:
    @staticmethod
    def isList(value: object):
        return isinstance(value, list)

    @staticmethod
    def isAnyNone(values: list) -> bool:
        for value in values:
            if value is None:
                return True
        return False