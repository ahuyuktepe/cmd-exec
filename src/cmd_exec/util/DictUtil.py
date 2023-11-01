
class DictUtil:

    @staticmethod
    def hasValue(obj: dict, key: str):
        return obj.get(key) is not None
