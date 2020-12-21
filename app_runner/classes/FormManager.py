from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.form_elements.FormElement import FormUIElement
from app_runner.utils.ListUtil import ListUtil


class FormManager:
    __fields: dict
    __activeIndex: int
    __page: int

    def __init__(self):
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

    def validateFormValues(self):
        fields: list = self.getAllFields()
        for field in fields:
            field.validate()

    def getValidationErrors(self) -> FieldValidationErrors:
        fields: list = self.getAllFields()
        errors: FieldValidationErrors = FieldValidationErrors()
        for field in fields:
            currentFieldErrors: FieldValidationErrors = field.getValidationErrors()
            errors.addErrors(currentFieldErrors.getErrors())
        return errors

    def isLastIndexOnCurrentPage(self) -> bool:
        return self.__activeIndex == self.getMaxIndexInCurrentPage()

    def isLastIndexOnLastPage(self) -> bool:
        return self.isLastPage() and self.isLastIndexOnCurrentPage()

    def isFirstIndexOnCurrentPage(self) -> bool:
        return self.__activeIndex == 0

    def isFirstIndexOnFirstPage(self) -> bool:
        return self.isFirstPage() and self.isFirstIndexOnCurrentPage()

    def isFirstPage(self) -> bool:
        return self.__page == 0

    def isLastPage(self) -> bool:
        pageCount = self.getPageCount()
        return self.__page == (pageCount - 1)

    def isActiveField(self, id: str) -> bool:
        field = self.getActiveField()
        return field is not None and field.getId() == id

    def areValuesValid(self) -> bool:
        errors: FieldValidationErrors = self.getValidationErrors()
        return not errors.hasErrors()

    def hasNextPage(self) -> bool:
        nextPage = self.__page + 1
        return self.__fields.get(nextPage) is not None

    def hasPreviousPage(self) -> bool:
        prePage = self.__page - 1
        return self.__fields.get(prePage) is not None

    # Setter Methods

    def addElement(self, page: int, element: FormUIElement):
        elementsByPage: list = self.__fields.get(page)
        if elementsByPage is None:
            elementsByPage = []
        elementsByPage.append(element)
        self.__fields[page] = elementsByPage

    # Utility Methods

    def reset(self):
        self.__fields.clear()
        self.__activeIndex = 0
        self.__page = 0

    def clearSelection(self):
        fields = self.getElementsInCurrentPage()
        for field in fields:
            field.setSelected(False)

    def updateSelection(self):
        self.clearSelection()
        activeField = self.getActiveField()
        activeField.setSelected(True)

    def increaseActiveIndex(self):
        if not self.isLastIndexOnCurrentPage():
            self.__activeIndex += 1
            self.updateSelection()

    def decreaseActiveIndex(self):
        if not self.isFirstIndexOnCurrentPage():
            self.__activeIndex -= 1
            self.updateSelection()

    def moveNextPage(self):
        if self.hasNextPage():
            self.__page += 1
            self.__activeIndex = 0

    def movePrePage(self):
        if self.hasPreviousPage():
            self.__page -= 1
            self.__activeIndex = 0
