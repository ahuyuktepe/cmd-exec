
class ListUtil:
    @staticmethod
    def isAnyNone(values: list) -> bool:
        for value in values:
            if value is None:
                return True
        return False

    @staticmethod
    def getElementByKey(elements: list, key: str, value: str) -> object:
        element: dict
        for element in elements:
            if element.get(key) == value:
                return element

    @staticmethod
    def getElementsByKey(elements: list, key: str, value: str) -> list:
        retList: list = []
        for element in elements:
            if element.get(key) == value:
                retList.append(element)
        return retList

    @staticmethod
    def removeElementByKey(elements: list, key: str, value: str) -> object:
        index = None
        for i in range(0, len(elements)):
            if elements[i].get(key) == value:
                index = i
                break
        return elements.pop(index)

    @staticmethod
    def hasElementByKey(elements: list, key: str, value: str) -> bool:
        element: object = ListUtil.getElementByKey(elements, key, value)
        return element is not None

    @staticmethod
    def mergeListsInGivenList(srcLists: list) -> list:
        retList: list = []
        for currentList in srcLists:
            retList += currentList
        return retList
