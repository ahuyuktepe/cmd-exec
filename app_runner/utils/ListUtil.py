from app_runner.utils.ErrorUtil import ErrorUtil

class ListUtil:
    @staticmethod
    def isAnyNone(values: list) -> bool:
        ErrorUtil.raiseExceptionIfNone(values)
        for value in values:
            if value is None:
                return True
        return False

    @staticmethod
    def getElementByKey(elements: list, key: str, value: str) -> object:
        ErrorUtil.raiseExceptionIfNone(elements)
        element: dict
        for element in elements:
            if element.get(key) == value:
                return element

    def getElementsByKey(self, elements: list, key: str, value: str) -> list:
        ErrorUtil.raiseExceptionIfNone(elements)
        retList: list = []
        for element in elements:
            if element.get(key) == value:
                retList.append(element)
        return retList

    @staticmethod
    def hasElementByKey(elements: list, key: str, value: str) -> bool:
        element: object = ListUtil.getElementByKey(elements, key, value)
        return element is not None
