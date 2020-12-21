from xml.etree.ElementTree import Element
from app_runner.builders.PrintAreaBuilder import PrintAreaBuilder
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.ui_elements.UIButtonGroup import UIButtonGroup
from app_runner.ui_elements.UILabel import UILabel
from app_runner.ui_elements.UISection import UISection
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil
from app_runner.utils.ValidationUtil import ValidationUtil
from app_runner.utils.XmlElementUtil import XmlElementUtil


class ElementBuilder:
    __printAreaBuilder: PrintAreaBuilder

    def __init__(self, printAreaBuilder: PrintAreaBuilder):
        self.__printAreaBuilder = printAreaBuilder

    def buildElements(self, xmlSectionElement: Element, section: UISection) -> list:
        elements: list = []
        xmlElements = xmlSectionElement.findall('*')
        for xmlElement in xmlElements:
            uiElement = None
            if xmlElement.tag == 'label':
                uiElement = self.__buildLabelElement(xmlElement, section)
            if uiElement is not None:
                elements.append(uiElement)
        return elements

    # Private Methods

    def __buildLabelElement(self, xmlElement: Element, section: UISection) -> UILabel:
        id = XmlElementUtil.getAttrValueAsStr(xmlElement, 'id', 'lbl')
        label = UILabel(id)
        # Set Dimensions and Beginning Point Location
        xStr = XmlElementUtil.getAttrValueAsStr(xmlElement, 'x', None)
        yStr = XmlElementUtil.getAttrValueAsStr(xmlElement, 'y', None)
        x = XmlElementUtil.calculateElementX(xStr, section.getWidth())
        y = XmlElementUtil.calculateElementY(yStr, section.getHeight())
        width = XmlElementUtil.getAttrValueAsInt(xmlElement, 'width', (section.getWidth() - x))
        height = 1
        # Set Printer
        sectionPrintArea = section.getPrintArea()
        # TODO: Validate
        ValidationUtil.failIfDerivedAreaWidthDoesNotFit((x+width), sectionPrintArea.getWidth())
        ValidationUtil.failIfDerivedAreaWidthDoesNotFit((y+height), sectionPrintArea.getHeight())
        labelPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(x, y, width, height, sectionPrintArea)
        label.setPrintArea(labelPrintArea)
        # Set Attributes
        label.setAttributes(xmlElement)
        return label

    # ============= Code To Be Enabled ==============

    # def __buildButtonGroupElement(self, element: Element, section: UISection) -> UIButtonGroup:
    #     id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'btn')
    #     btnGrp = UIButtonGroup(id)
    #     # Set Printer
    #     sectionPrintArea: UIPrintArea = section.getPrintArea()
    #     btnGrp.setPrintArea(sectionPrintArea)
    #     # Set Attributes
    #     btnGrp.setAttributes(element)
    #     # Set Buttons
    #     index = 1
    #     btns = []
    #     for btnElement in element.iter('button'):
    #         btnId = btnGrp.getId() + '-btn-' + str(index)
    #         evnt = 'buttonClicked' + str(index)
    #         btns.append({
    #             'id': XmlElementUtil.getAttrValueAsStr(btnElement, 'id', btnId),
    #             'event': XmlElementUtil.getAttrValueAsStr(btnElement, 'event', evnt),
    #             'label': btnElement.text
    #         })
    #     btnGrp.setButtons(btns)
    #     return btnGrp

    # def __buildElementsInSection(self, element: Element, section: UISection, data: dict = {}) -> list:
    #     elements: list = []
    #     for child in element:
    #         uiElement = None
    #         if child.tag == 'label':
    #             uiElement = self.__buildLabelElement(child, section)
    #         elif child.tag == 'button-group':
    #             uiElement = self.__buildButtonGroupElement(child, section)
    #         elif child.tag == 'cmd-selector':
    #             uiElement = self.__buildCmdSelectorElement(child, section)
    #             # Set Top Menu
    #             topMenu = self.__buildTopMenu(uiElement, child)
    #             topMenu.initialize()
    #             # Set Menus
    #             menus = self.__buildMenus(child, data)
    #             topMenu.addMenus(menus)
    #             uiElement.setTopMenu(topMenu)
    #             # Set Command Menu
    #             cmdMenu = self.__buildCmdMenu(uiElement)
    #             uiElement.setCmdMenu(cmdMenu)
    #         elif child.tag == 'form':
    #             uiElement = self.__buildFormElement(child, section, data)
    #         elif child.tag == 'html':
    #             uiElement = self.__buildHtmlElement(child, section, data)
    #         elif child.tag == 'text':
    #             uiElement = self.__buildTextElement(child, section)
    #         if uiElement is not None:
    #             elements.append(uiElement)
    #     return elements

    # def __buildTopMenu(self, uiElement: UICmdSelector, xmlElement: Element) -> UITopMenu:
    #     # Set Top Menu
    #     topMenuNameWidth = XmlElementUtil.getAttrValueAsInt(xmlElement, 'topMenuNameWidth', 20)
    #     topMenu = UITopMenu(topMenuNameWidth)
    #     printArea = UIPrintAreaUtil.buildDerivedPrintArea(0, 0, uiElement.getWidth(), 2, uiElement.getPrintArea())
    #     topMenu.setPrintArea(printArea)
    #     return topMenu

    # def __buildCmdMenu(self, uiElement: UICmdSelector) -> UICmdMenu:
    #     # Set Command Menu
    #     cmdMenu = UICmdMenu()
    #     width = 40
    #     height = 13
    #     horizontalPadding = math.floor((uiElement.getHeight() - height) / 2)
    #     verticalPadding = math.floor((uiElement.getWidth() - width) / 2)
    #     printArea = UIPrintAreaUtil.buildDerivedPrintArea(verticalPadding, horizontalPadding, width, height, uiElement.getPrintArea())
    #     cmdMenu.setPrintArea(printArea)
    #     return cmdMenu

    # def __buildTextElement(self, element: Element, section: UISection):
    #     id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'text')
    #     text = UIText(id)
    #     text.setAttributes(element)
    #     # Set Dimensions
    #     width = XmlElementUtil.getAttrValueAsInt(element, 'width', section.getWidth() - 2)
    #     height = XmlElementUtil.getAttrValueAsInt(element, 'height', section.getHeight() - 2)
    #     # Set Printer
    #     sectionPrintArea: UIPrintArea = section.getPrintArea()
    #     printArea: UIPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(1, 1, width, height, sectionPrintArea)
    #     text.setPrintArea(printArea)
    #     return text

    # def __buildCmdSelectorElement(self, element: Element, section: UISection) -> UICmdSelector:
    #     id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'menu')
    #     uiElement = UICmdSelector(id)
    #     # Set Printer
    #     sectionPrintArea: UIPrintArea = section.getPrintArea()
    #     width = section.getWidth() - 2
    #     height = section.getHeight() - 1
    #     elementPrintArea: UIPrintArea = UIPrintAreaUtil.buildDerivedPrintArea(1, 1, width, height, sectionPrintArea)
    #     uiElement.setPrintArea(elementPrintArea)
    #     # Save Xml Tag Attributes
    #     uiElement.setAttributes(element)
    #     return uiElement

    # def __buildFormElement(self, element: Element, section: UISection, data: dict = {}) -> UIForm:
    #     id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'form')
    #     uiElement = UIForm(id, self.__fieldService)
    #     # Set Printer
    #     sectionPrintArea: UIPrintArea = section.getPrintArea()
    #     formPrintArea = UIPrintAreaUtil.
    #     uiElement.setPrintArea(formPrintArea)
    #     return uiElement

    # def __buildMenus(self, element: Element, data: dict = {}) -> list:
    #     # Set Menus
    #     menuIdsStr = data.get('menus')
    #     if menuIdsStr is None:
    #         menuIdsStr = XmlElementUtil.getAttrValueAsStr(element, 'menus', '')
    #     menus = self.__menuService.buildMenusFromCommaSeparatedIds(menuIdsStr)
    #     return menus

    # def __buildHtmlElement(self, element: Element, section: UISection, data: dict = {}) -> UIHtml:
    #     id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'text-area')
    #     uiElement = UIHtml(id)
    #     # Set Printer
    #     sectionPrintArea: UIPrintArea = section.getPrintArea()
    #     formPrintArea = UIPrintAreaUtil.buildFullCoverageDerivedPrintArea(sectionPrintArea)
    #     uiElement.setPrintArea(formPrintArea)
    #     return uiElement

    # def __addSelectableUIElementsToView(self, view: UIView, uiElements: list):
    #     for uiElement in uiElements:
    #         if uiElement.isSelectable():
    #             view.addUIElement(uiElement)
