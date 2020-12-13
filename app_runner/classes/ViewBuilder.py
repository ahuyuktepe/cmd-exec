import math
from xml.etree.ElementTree import ElementTree, Element
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.menu.Command import Command
from app_runner.services.FieldService import FieldService
from app_runner.services.MenuService import MenuService
from app_runner.ui_elements.UICmdMenu import UICmdMenu
from app_runner.ui_elements.UICmdSelector import UICmdSelector
from app_runner.ui_elements.UIForm import UIForm
from app_runner.ui_elements.UILabel import UILabel
from app_runner.ui_elements.UISection import UISection
from app_runner.ui_elements.UIText import UIText
from app_runner.ui_elements.UITopMenu import UITopMenu
from app_runner.ui_elements.UIView import UIView
from app_runner.ui_elements.UlXml import UIHtml
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil
from app_runner.utils.ValidationUtil import ValidationUtil
from app_runner.utils.XmlElementUtil import XmlElementUtil


class ViewBuilder:
    __menuService: MenuService
    __fieldService: FieldService

    def __init__(self, menuService: MenuService, fieldService: FieldService):
        self.__menuService = menuService
        self.__fieldService = fieldService

    def buildView(self, printArea: UIPrintArea, vid: str, data: dict = {}) -> UIView:
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
                    if srcSection.get('hide') == 'true':
                        templateRoot.remove(destSection)
                    XmlElementUtil.copyChildren(srcSection, destSection)
                    XmlElementUtil.overwriteAttributes(srcSection, destSection)
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
            uiElement = None
            if child.tag == 'label':
                uiElement = self.__buildLabelElement(child, section)
            elif child.tag == 'cmd-selector':
                uiElement = self.__buildCmdSelectorElement(child, section)
                menus = self.__buildMenus(child, data)
                uiElement.setMenus(menus)
                # Set Top Menu
                topMenu = self.__buildTopMenu(uiElement, child)
                topMenu.initialize()
                uiElement.setTopMenu(topMenu)
                # Set Command Menu
                cmdMenu = self.__buildCmdMenu(uiElement)
                uiElement.setCmdMenu(cmdMenu)
            elif child.tag == 'form':
                uiElement = self.__buildFormElement(child, section, data)
            elif child.tag == 'html':
                uiElement = self.__buildHtmlElement(child, section, data)
            elif child.tag == 'text':
                uiElement = self.__buildTextElement(child, section)
            if uiElement is not None:
                elements.append(uiElement)
        return elements

    def __buildTopMenu(self, uiElement: UICmdSelector, xmlElement: Element) -> UITopMenu:
        # Set Top Menu
        topMenuNameWidth = XmlElementUtil.getAttrValueAsInt(xmlElement, 'topMenuNameWidth', 20)
        topMenu = UITopMenu(topMenuNameWidth)
        printArea = UIPrintAreaUtil.buildDerivedPrintArea(0, 0, uiElement.getWidth(), 2, uiElement.getPrintArea())
        topMenu.setPrintArea(printArea)
        return topMenu

    def __buildCmdMenu(self, uiElement: UICmdSelector) -> UICmdMenu:
        # Set Command Menu
        cmdMenu = UICmdMenu()
        width = 40
        height = 13
        horizontalPadding = math.floor((uiElement.getHeight() - height) / 2)
        verticalPadding = math.floor((uiElement.getWidth() - width) / 2)
        printArea = UIPrintAreaUtil.buildDerivedPrintArea(verticalPadding, horizontalPadding, width, height, uiElement.getPrintArea())
        cmdMenu.setPrintArea(printArea)
        return cmdMenu

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

    def __buildTextElement(self, element: Element, section: UISection):
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'text')
        text = UIText(id)
        text.setAttributes(element)
        # Set Dimensions
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', section.getWidth() - 2)
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', section.getHeight() - 2)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        printArea: UIPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(1, 1, width, height, sectionPrintArea)
        text.setPrintArea(printArea)
        return text

    def __buildLabelElement(self, element: Element, section: UISection) -> UILabel:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'lbl')
        label = UILabel(id)
        label.setAttributes(element)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        label.setPrintArea(sectionPrintArea)
        return label

    def __buildCmdSelectorElement(self, element: Element, section: UISection) -> UICmdSelector:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'menu')
        uiElement = UICmdSelector(id)
        # Set Printer
        sectionPrintArea: UIPrintArea = section.getPrintArea()
        width = section.getWidth() - 2
        height = section.getHeight() - 1
        elementPrintArea: UIPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(1, 1, width, height, sectionPrintArea)
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
