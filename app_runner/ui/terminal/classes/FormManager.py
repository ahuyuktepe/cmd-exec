from app_runner.ui.terminal.form.FormUIElement import FormUIElement
from app_runner.utils.ListUtil import ListUtil


class FormManager:
    __fields: dict
    __activeIndex: int
    __page: int

    def __init__(self, width: int, height: int):
        self.__height = height
        self.__width = width
        self.__fields = {}
        self.__activeIndex = 0
        self.__page = 0

    # Getter Methods

    def getAllFields(self) -> list:
        values = self.__fields.values()
        return ListUtil.mergeListsInGivenList(values)

    def getActiveField(self) -> FormUIElement:
        fields: list = self.getElementsInCurrentPage()
        if fields is not None:
            return fields[self.__activeIndex]

    def getElementsInCurrentPage(self) -> list:
        return self.__fields.get(self.__page)

    def getMaxIndexInCurrentPage(self) -> int:
        elements: list = self.getElementsInCurrentPage()
        return len(elements) - 1

    def getPage(self) -> int:
        return self.__page

    def getPageCount(self) -> int:
        return len(list(self.__fields.keys()))

    def isLastIndexOnCurrentPage(self) -> bool:
        return self.__activeIndex == self.getMaxIndexInCurrentPage()

    def isFirstIndexOnCurrentPage(self) -> bool:
        return self.__activeIndex == 0

    def isLastPage(self) -> bool:
        pageCount = self.getPageCount()
        return self.__page == (pageCount - 1)

    def hasNextPage(self) -> bool:
        nextPage = self.__page + 1
        return self.__fields.get(nextPage) is not None

    def hasPreviousPage(self) -> bool:
        prePage = self.__page - 1
        return self.__fields.get(prePage) is not None

    # Utility Methods

    def reset(self):
        self.__fields.clear()
        self.__activeIndex = 0
        self.__page = 0

    def clearFields(self):
        fields = self.getElementsInCurrentPage()
        for field in fields:
            field.clear()
            field.refresh()

    def clearBorders(self):
        fields = self.getElementsInCurrentPage()
        for field in fields:
            field.setBorder(False)

    def highlightActiveField(self):
        self.clearBorders()
        field: FormUIElement = self.getActiveField()
        field.setBorder(True)

    def increaseActiveIndex(self):
        if not self.isLastIndexOnCurrentPage():
            self.__activeIndex += 1
        elif self.isLastIndexOnCurrentPage() and self.hasNextPage():
            self.__activeIndex = 0
            self.__page += 1

    def decreaseActiveIndex(self):
        if not self.isFirstIndexOnCurrentPage():
            self.__activeIndex -= 1
        elif self.isFirstIndexOnCurrentPage() and self.hasPreviousPage():
            self.__page -= 1
            self.__activeIndex = self.getMaxIndexInCurrentPage()

    def moveNextPage(self):
        if self.hasNextPage():
            self.__page += 1
            self.__activeIndex = 0

    def movePrePage(self):
        if self.hasPreviousPage():
            self.__page -= 1
            self.__activeIndex = 0

    # Private Methods

    def addElement(self, page: int, element: FormUIElement):
        elementsByPage: list = self.__fields.get(page)
        if elementsByPage is None:
            elementsByPage = []
        elementsByPage.append(element)
        self.__fields[page] = elementsByPage
