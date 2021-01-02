
class ListUtil:

    @staticmethod
    def getByIndex(arr: list, index: int, defVal: object = None):
        maxIndex = len(arr) - 1
        if maxIndex < index:
            return defVal
        return arr[index]
