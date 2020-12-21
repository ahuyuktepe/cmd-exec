from app_runner.classes.FormManager import FormManager
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.errors.AppRunnerError import AppRunnerError
from app_runner.field.Field import Field
from app_runner.form_elements.FormElement import FormUIElement
from app_runner.form_elements.MultiChoiceFormElement import MultiChoiceFormElement
from app_runner.form_elements.TextFormElement import TextElement
from app_runner.services.FieldService import FieldService
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil


class FormElementBuilder:
    __formManager: FormManager
    __fieldService: FieldService
    __formHeight: int
    __formWidth: int
    __formPrintArea: UIPrintArea
    __currentY: int
    __currentPage: int

    def __init__(self, formManager: FormManager, formPrintArea: UIPrintArea, fieldService: FieldService):
        self.__formManager = formManager
        self.__fieldService = fieldService
        self.__formPrintArea = formPrintArea

    def refreshElements(self):
        elements = self.__formManager.getAllFields().copy()
        self.reset()
        # Visit each element
        for element in elements:
            self.__updateElementProperties(element)
            self.__formManager.addElement(self.__currentPage, element)

    def reset(self):
        self.__formManager.reset()
        self.__formHeight = self.__formPrintArea.getHeight() - 3
        self.__formWidth = self.__formPrintArea.getWidth() - 2
        self.__currentY = 1
        self.__currentPage = 0

    def buildElementsAndAdd(self, field: Field):
        if field.isText():
            element = TextElement(field, self.__fieldService)
            self.__updateElementProperties(element)
            self.__formManager.addElement(self.__currentPage, element)
        elif field.isSingleSelect():
            element = MultiChoiceFormElement(field, False, self.__fieldService)
            self.__updateElementProperties(element)
            self.__formManager.addElement(self.__currentPage, element)
        elif field.isMultiSelect():
            element = MultiChoiceFormElement(field, True, self.__fieldService)
            self.__updateElementProperties(element)
            self.__formManager.addElement(self.__currentPage, element)

    # Private Methods

    def __updateElementProperties(self, element: FormUIElement):
        width = self.__formWidth
        height = element.getCalculatedHeight()
        self.__updatePage(height)
        printArea = UIPrintAreaUtil.buildDerivedPrintArea(1, self.__currentY, width, height, self.__formPrintArea)
        element.setPrintArea(printArea)
        self.__currentY += height

    def __updatePage(self, height: int):
        bottomY = self.__currentY + height
        if bottomY >= self.__formHeight:
            self.__currentY = 2
            self.__currentPage += 1

    def __failIfHeightIsBiggerThanFormHeight(self, height: int):
        if height >= self.__formHeight:
            raise AppRunnerError("Form element's height '" + str(height) + "' exceeds form's height (" + str(self.__formHeight) + ").")
