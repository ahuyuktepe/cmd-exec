from app_runner.classes.FormManager import FormManager
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.errors.UIError import UIError
from app_runner.field.Field import Field
from app_runner.form_elements.FormUIElement import FormUIElement
from app_runner.form_elements.TextElement import TextElement
from app_runner.services.FieldService import FieldService
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class FormElementBuilder:
    __formManager: FormManager
    __fieldService: FieldService
    __formHeight: int
    __formWidth: int
    __formPrintArea: UIPrintArea
    __mid: str
    __currentY: int
    __currentPage: int

    def __init__(self, formManager: FormManager, formPrintArea: UIPrintArea, fieldService: FieldService, mid: str):
        self.__formManager = formManager
        self.__fieldService = fieldService
        self.__formPrintArea = formPrintArea
        self.__mid = mid

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
            element = TextElement(field, self.__mid, self.__fieldService)
            self.__updateElementProperties(element)
            self.__formManager.addElement(self.__currentPage, element)

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
            raise UIError("Form element's height '" + str(height) + "' exceeds form's height (" + str(self.__formHeight) + ").")
