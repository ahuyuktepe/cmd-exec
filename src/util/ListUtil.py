
class ListUtil:

    @staticmethod
    def getByIndex(arr: list, index: int, defVal: object = None):
        maxIndex = len(arr) - 1
        if maxIndex < index:
            return defVal
        return arr[index]

    @staticmethod
    def deleteElements(arr: list, elementsToDelete: list = []):
        for element in arr:
            if element in elementsToDelete:
                arr.remove(element)
