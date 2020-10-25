import curses
from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.field.Field import Field
from app_runner.menu.Command import Command
from app_runner.ui.terminal.classes.FormManager import FormManager
from app_runner.ui.terminal.form.FormUIElement import FormUIElement
from app_runner.ui.terminal.form.MultiChoiceElement import MultiChoiceElement
from app_runner.ui.terminal.form.TextElement import TextElement
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.StrUtil import StrUtil


class FormElement(UIElement):
    __manager: FormManager
    __startY = 2
    __cmd: Command
    __errors: FieldValidationErrors
    __values: dict

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'form', appContext)
        self.__values = {}
        self.__errors = FieldValidationErrors()

    # Setter Methods

    def setAttributes(self, element: Element):
        parent = self.getParent()
        # Set Dimensions
        parentWidth = parent.getWidth() - 5
        parentHeight = parent.getHeight() - 2
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', parentWidth)
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', parentHeight)
        if width > parentWidth:
            width = parentWidth
        elif height > parentHeight:
            height = parentHeight
        self.setDimensions(width, height)
        # Set Locations
        self.setLocation(0, 0)
        super().setAttributes(element)
        self.__manager = FormManager(self.getWidth(), self.getHeight())

    def setListeners(self):
        EventManager.listenEvent(UIEventType.COLLECT_FIELD_VALUES, self)

    # Event Listeners

    def collectFieldValues(self, data: dict):
        self.__cmd = data.get('command')
        fields: list = list(self.__cmd.getFields().values())
        while True:
            # Build Form Elements
            self.__buildFormElements(fields)
            # Print fields
            self.__printFields()
            # Collect User Entries
            self.__getFormValuesFromUser()
            # Validate Values
            # self.__validateValues()
            # Exit If Valid
            if self.__isValid():
                break
        # Print Values
        print(str(self.__values))

    # Private Methods

    def __isValid(self) -> bool:
        return not self.__errors.hasErrors()

    def __validateValues(self):
        self.__errors.clearErrors()
        element: FormUIElement
        for element in self.__manager.getAllFields():
            errors = element.validate(self.__cmd)
            self.__errors.addErrors(errors.getErrors())

    def __getFormValuesFromUser(self):
        userInput: dict = self.__getUserInput()
        while userInput['action'] != 'submit':
            field = userInput['field']
            self.__values[field.getId()] = field.getUserInput()
            userInput: dict = self.__getUserInput()

    def __buildFormElements(self, fields: list):
        if fields is not None:
            availableHeight = self.getHeight() - 3
            y = self.__startY
            page = 0
            element: UIElement
            for field in fields:
                if y >= availableHeight:
                    y = self.__startY
                    page += 1
                if field.isText():
                    element = self.__buildTextElement(field, y, 2)
                elif field.isSingleSelect():
                    element = self.__buildMultiChoiceElement(field, y, 2)
                elif field.isMultiSelect():
                    element = self.__buildMultiChoiceElement(field, y, 2, True)
                if element is not None:
                    self.__manager.addElement(page, element)
                    y = element.getBottomY()

    def __buildTextElement(self, field: Field, y: int, x: int) -> TextElement:
        element = TextElement(field, self._appContext)
        element.setLocation(x, y)
        element.setDimensions(self.getWidth(), 5)
        element.setParent(self)
        element.initFromParent()
        return element

    def __buildMultiChoiceElement(self, field: Field, y: int, x: int, isMultiSelect: bool = False) -> MultiChoiceElement:
        element = MultiChoiceElement(field, self._appContext, isMultiSelect)
        element.setLocation(x, y)
        height = len(field.getOptions()) + 4
        element.setDimensions(self.getWidth(), height)
        element.setParent(self)
        element.initFromParent()
        return element

    def __printFields(self):
        self.printFormHeader()
        self.__manager.highlightActiveField()
        elements: list = self.__manager.getElementsInCurrentPage()
        for element in elements:
            element.print()

    def __getUserInput(self) -> dict:
        userInput: dict = {}
        curses.cbreak()
        curses.noecho()
        exitWhile = False
        while not exitWhile :
            selection = self._window.get_wch()
            if selection == 'w':
                self.__manager.clearFields()
                self.__manager.decreaseActiveIndex()
                self.__printFields()
            elif selection == 's':
                self.__manager.clearFields()
                self.__manager.increaseActiveIndex()
                self.__printFields()
            elif selection == 'a':
                self.__manager.clearFields()
                self.__manager.movePrePage()
                self.__printFields()
            elif selection == 'd':
                self.__manager.clearFields()
                self.__manager.moveNextPage()
                self.__printFields()
            elif selection == 'e':
                userInput['field'] = self.__manager.getActiveField()
                userInput['action'] = 'field-selection'
                exitWhile = True
            elif selection == 'q':
                userInput['action'] = 'submit'
                exitWhile = True
        return userInput

    def printFormHeader(self):
        title = StrUtil.getAlignedAndLimitedStr(self.__cmd.getDescription(), self.getWidth(), 'center')
        self._window.addstr(1, 1, title)
        self.__printPageInfo()
        self.refresh()

    def __printPageInfo(self):
        pageCount = self.__manager.getPageCount()
        currentPage = self.__manager.getPage() + 1
        if pageCount != 1:
            pageInfo = 'page ' + str(currentPage) + '/' + str(pageCount)
            x = self.getWidth() - len(pageInfo) + 1
            self._window.addstr(1, x, pageInfo)
