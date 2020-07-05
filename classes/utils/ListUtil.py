
class ListUtil:
    @staticmethod
    def isAnyNone(values: list) -> bool:
        for value in values:
            if value is None:
                return True
        return False

    @staticmethod
    def getElementByKey(self, elements: list, key: str, value: str):
        element: dict
        for element in elements:
            if element.get(key) == value:
                return element
