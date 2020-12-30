import math
from xml.etree.ElementTree import Element
from app_runner.builders.ElementBuilder import ElementBuilder
from app_runner.builders.PrintAreaBuilder import PrintAreaBuilder
from app_runner.ui_elements.UISection import UISection
from app_runner.ui_elements.UIView import UIView
from app_runner.utils.XmlElementUtil import XmlElementUtil


class SectionBuilder:
    __elementBuilder: ElementBuilder
    __printAreaBuilder: PrintAreaBuilder

    def __init__(self, elementBuilder: ElementBuilder, printAreaBuilder: PrintAreaBuilder):
        self.__elementBuilder = elementBuilder
        self.__printAreaBuilder = printAreaBuilder

    def buildSections(self, rootXmlElement: Element, view: UIView):
        # Build Sections
        sectionElements = rootXmlElement.findall('*')
        for element in sectionElements:
            if element.tag == 'section':
                self.__buildSectionAndInsertIntoView(element, view)
            elif element.tag == 'divided-sections':
                self.__buildSectionsAndInsertIntoView(element, view)

    # Private Methods

    def __buildSectionAndInsertIntoView(self, element: Element, view: UIView):
        # Set X and Y
        x = 0
        y = self.__getNextY(view)
        section = self.__generateSection(element)
        # Set Dimensions
        height = self.__getHeight(element, view)
        width = view.getWidth()
        # Set Print Area
        printArea = self.__printAreaBuilder.buildDerivedPrintArea(x, y, width, height, view.getPrintArea())
        section.setPrintArea(printArea)
        # Build and Insert Elements
        self.__buildElementsAndInsert(element, view, section)
        view.addSection(section)

    def __buildElementsAndInsert(self, element: Element, view: UIView, section: UISection):
        uiElements: list = self.__elementBuilder.buildElements(element, section)
        for uiElement in uiElements:
            section.addElement(uiElement)

    def __buildSectionsAndInsertIntoView(self, element: Element, view: UIView):
        # Set Dimensions
        height = self.__getHeight(element, view)
        cols = XmlElementUtil.getAttrValueAsInt(element, 'cols', 1)
        colWidth = math.floor(view.getWidth() / cols)
        # Set X and Y
        x = 0
        y = self.__getNextY(view)
        # Initiate Sections
        sections = element.findall('./section')
        order = 1
        for sectionElement in sections:
            section = self.__generateSection(sectionElement)
            # Set Width
            colSpan = XmlElementUtil.getAttrValueAsInt(sectionElement, 'colspan', 1)
            width = colSpan * colWidth
            isLastElement = (order > 1 and order == len(sections))
            if isLastElement:
                previousSection = view.getLastSection()
                width = view.getWidth() - (previousSection.getX() + previousSection.getWidth()) + 1
            # Set Print Area
            printArea = self.__printAreaBuilder.buildDerivedPrintArea(x, y, width, height, view.getPrintArea())
            section.setPrintArea(printArea)
            # Build and Insert Elements
            self.__buildElementsAndInsert(sectionElement, view, section)
            # Add Section To View
            view.addSection(section)
            # Prepare Variables For Next Loop
            x += width - 1
            order += 1

    def __getHeight(self, element: Element, view: UIView) -> int:
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', 3)
        if height < 0:
            height = view.getHeight() + height
        return height

    def __generateSection(self, element: Element) -> UISection:
        # Initialize Section
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'section')
        section = UISection(id)
        section.setAttributes(element)
        return section

    def __getNextY(self, view: UIView) -> int:
        sections = view.getSections()
        if len(sections) > 0:
            section: UISection = sections[-1]
            return section.getY() + section.getHeight() - 1
        return 0
