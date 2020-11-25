import math
from xml.etree.ElementTree import ElementTree, Element
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Command import Command
from app_runner.services.FieldService import FieldService
from app_runner.services.MenuService import MenuService
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.ui_elements.UIHtml import UIHtml
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil
from app_runner.classes.ViewManager import ViewManager
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UIForm import UIForm
from app_runner.ui_elements.UIMenu import UIMenu
from app_runner.ui_elements.UIMenuSelection import UIMenuSelection
from app_runner.ui_elements.UINavigation import UINavigation
from app_runner.ui_elements.UISection import UISection
from app_runner.ui_elements.UIText import UIText
from app_runner.ui_elements.UIView import UIView
from app_runner.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class UIScreen(UIElement):
    __menuService: MenuService
    __fieldService: FieldService
    __viewManager: ViewManager
    __selectedCmd: Command
    __collectedFieldValues: dict

    def __init__(self, menuService: MenuService, fieldService: FieldService):
        super().__init__('root-screen', 'screen')
        self.__menuService = menuService
        self.__fieldService = fieldService
        self.__viewManager = ViewManager()
        self.__selectedCmd = None

    def displayView(self, vid: str, data: dict = {}):
        view: UIView = self.__viewManager.getView(vid)
        if view is None:
            view = self.__buildView(vid, data)
        self.__viewManager.addAndActivateView(view)
        self.setListeners()
        view.display()

    def getSelectedCommand(self, data: dict = {}) -> Command:
        self.displayView('menu', data)
        return self.__selectedCmd

    def collectFieldValues(self, cmd: Command) -> dict:
        self.displayView('form', {
            'command': cmd
        })
        EventManager.triggerEvent(UIEventType.COLLECT_FIELD_VALUES)
        return self.__collectedFieldValues

    def displayHtml(self, html: str):
        self.displayView('html')
        EventManager.triggerEvent(UIEventType.DISPLAY_HTML, {
            'html': html
        })

    # Utility Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.COMMAND_SELECTED, self)
        EventManager.listenEvent(UIEventType.FIELD_VALUES_COLLECTED, self)

    # Event Handlers

    def commandSelected(self, data: dict):
        cmd: Command = data.get('command')
        if cmd.hasNextMenus():
            mids = cmd.getMenus()
            menus = self.__menuService.buildMenus(mids)
            EventManager.triggerEvent(UIEventType.DISPLAY_MENUS, {
                'menus': menus
            })
        else:
            self.__viewManager.closeActiveView()
            self.__selectedCmd = cmd

    def fieldValuesCollected(self, data: dict):
        self.__collectedFieldValues = data.get('values')

    # Private Methods

    def __buildView(self, vid: str, data: dict = {}) -> UIView:
        # Build Object From Xml
        fileName = vid + ".view.xml"
        filePath = FileUtil.getAbsolutePath(['resources', 'views', fileName])
        elementTree: ElementTree = FileUtil.generateObjFromFile(filePath)
        root: Element = elementTree.getroot()
        # Merge Template
        template = XmlElementUtil.getAttrValueAsStr(root, 'template', None)
        if template is not None:
            root = self.__mergeViewIntoTemplate(template, root)
        # Build View
        id = XmlElementUtil.getAttrValueAsStr(root, 'id', vid)
        view: UIView = UIView(id)
        view.setAttributes(root)
        # Build and Set Printer
        printArea: UIPrintArea = UIPrintAreaUtil.buildScreenPrintArea()
        view.setPrintArea(printArea)
        # Build Sections
        self.__buildSectionsForView(root, view, data)
        return view

    def __mergeViewIntoTemplate(self, template: str, viewElement: Element) -> Element:
        # Read Template File
        templateFileName = template + '.template.xml'
        filePath = FileUtil.getAbsolutePath(['resources', 'views', templateFileName])
        tempTree: ElementTree = FileUtil.generateObjFromFile(filePath)
        templateRoot = tempTree.getroot()
        # Visit Each Element
        destSections = templateRoot.findall('./section[@ref]')
        for destSection in destSections:
            ref = XmlElementUtil.getAttrValueAsStr(destSection, 'ref', None)
            if ref is not None:
                destSection.set('ref', None)
                srcSections = viewElement.findall("./section[@id='" + ref + "']")
                for srcSection in srcSections:
                    XmlElementUtil.copyChildren(srcSection, destSection)
        return templateRoot

    def __buildSectionsForView(self, element: Element, view: UIView, data: dict):
        # Build Sections
        sectionElements = element.findall('./section')
        for element in sectionElements:
            section = self.__buildSectionInView(element, view)
            elements = self.__buildElementsInSection(element, section, data)
            section.setElements(elements)
            view.addSection(section)

    def __buildElementsInSection(self, element: Element, section: UISection, data: dict = {}) -> list:
        elements: list = []
        for child in element:
            if child.tag == 'text':
                uiElement = self.__buildTextElement(child, section)
                elements.append(uiElement)
            elif child.tag == 'navigation':
                uiElement = self.__buildNavigationElement(child, section)
                menus = self.__buildMenus(child, data)
                uiElement.setMenus(menus)
                elements.append(uiElement)
            elif child.tag == 'menu-selection':
                uiElement = self.__buildMenuSelectionElement(child, section)
                elements.append(uiElement)
            elif child.tag == 'menu':
                uiElement = self.__buildMenuElement(child, section)
                elements.append(uiElement)
            elif child.tag == 'form':
                uiElement = self.__buildFormElement(child, section, data)
                elements.append(uiElement)
            elif child.tag == 'html':
                uiElement = self.__buildHtmlElement(child, section, data)
                elements.append(uiElement)
        return elements

    def __buildSectionInView(self, element: Element, view: UIView) -> UISection:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        section = UISection(id)
        section.setAttributes(element)
        # Set Dimensions
        x = 0
        y = view.getBottomY()
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', view.getWidth() - x)
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', view.getHeight() - y)
        if height < 0:
            height = view.getHeight() + height
        # Validate If section
        ValidationUtil.failIfSectionHeightDoesNotFitIntoView(y, height, view.getHeight())
        ValidationUtil.failIfSectionWidthDoesNotFitIntoView(x, width, view.getWidth())
        # Set Printer
        viewPrintArea: UIPrintArea = view.getPrintArea()
        sectionPrintArea: UIPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(x, y, width, height, viewPrintArea)
        section.setPrintArea(sectionPrintArea)
        return section

    def __buildTextElement(self, element: Element, section: UISection) -> UIText:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'lbl')
        label = UIText(id)
        label.setAttributes(element)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        label.setPrintArea(sectionPrintArea)
        return label

    def __buildNavigationElement(self, element: Element, section: UISection) -> UINavigation:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'navigation')
        uiElement = UINavigation(id)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        elementPrintArea: UIPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(1, 1, section.getWidth() - 2, 2, sectionPrintArea)
        uiElement.setPrintArea(elementPrintArea)
        uiElement.setAttributes(element)
        return uiElement

    def __buildMenuSelectionElement(self, element: Element, section: UISection) -> UIMenuSelection:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'menu-selection')
        uiElement = UIMenuSelection(id)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        uiElement.setPrintArea(sectionPrintArea)
        uiElement.setAttributes(element)
        return uiElement

    def __buildMenuElement(self, element: Element, section: UISection) -> UIMenuSelection:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'menu')
        uiElement = UIMenu(id)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        # Set Dimensions
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', 40)
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', 10)
        x = math.floor((section.getWidth() - width) / 2)
        y = math.floor((section.getHeight() - height) / 2)
        # Set Print Area
        elementPrintArea: UIPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(x, y, width, height, sectionPrintArea)
        uiElement.setPrintArea(elementPrintArea)
        # Save Xml Tag Attributes
        uiElement.setAttributes(element)
        return uiElement

    def __buildFormElement(self, element: Element, section: UISection, data: dict = {}) -> UIForm:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'form')
        cmd: Command = data.get('command')
        uiElement = UIForm(id, cmd.getDescription(), cmd, self.__fieldService)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        formPrintArea = UIPrintAreaUtil.buildFullCoverageDerivedPrintArea(sectionPrintArea)
        uiElement.setPrintArea(formPrintArea)
        return uiElement

    def __buildMenus(self, element: Element, data: dict = {}) -> list:
        # Set Menus
        menuIdsStr = data.get('menus')
        if menuIdsStr is None:
            menuIdsStr = XmlElementUtil.getAttrValueAsStr(element, 'menus', '')
        menus = self.__menuService.buildMenusFromCommaSeparatedIds(menuIdsStr)
        return menus

    def __buildHtmlElement(self, element: Element, section: UISection, data: dict = {}) -> UIHtml:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'text-area')
        uiElement = UIHtml(id)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        formPrintArea = UIPrintAreaUtil.buildFullCoverageDerivedPrintArea(sectionPrintArea)
        uiElement.setPrintArea(formPrintArea)
        return uiElement
