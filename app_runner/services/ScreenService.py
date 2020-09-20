from xml.etree.ElementTree import ElementTree, Element
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.element.UIScreen import UIScreen
from app_runner.ui.terminal.element.UIView import UIView
from app_runner.ui.terminal.element.UISection import UISection
from app_runner.ui.terminal.utils.UIElementUtil import UIElementUtil
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.FileUtil import FileUtil


class ScreenService:

    def buildView(self, sid: str) -> UIView:
        # Initialize View
        view: UIView = UIView('root')
        view.initialize()
        # Build Object From Xml
        filePath = FileUtil.getAbsolutePath(['resources', 'terminal', 'views', sid])
        elementTree: ElementTree = FileUtil.generateObjFromFile(filePath + '.xml')
        root: Element = elementTree.getroot()
        # Populate Sections
        self.__populateSectionsFromXml(root, view)
        return view

    def __populateSectionsFromXml(self, root: Element, screen: UIView):
        sections = root.findall('./section')
        y = 0
        for element in sections:
            section: UISection = self.__initializeSection(element)
            width = XmlElementUtil.getAttrValueAsInt(element, 'width', screen.getWidth())
            height = XmlElementUtil.getAttrValueAsInt(element, 'height', screen.getHeight())
            section.setDimensions(width, height)
            section.setLocation(0, y)
            section.initialize()
            y += section.getHeight()-1
            self.__populateSectionElements(element, section)
            screen.addSection(section)

    def __initializeSection(self, element: Element) -> UISection:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        cols = XmlElementUtil.getAttrValueAsInt(element, 'cols', 1)
        rows = XmlElementUtil.getAttrValueAsInt(element, 'cols', 1)
        section = UISection(id, cols, rows)
        return section

    def __populateSectionElements(self, element: Element, section: UISection):
        uiElement: UIElement = None
        for child in element:
            if child.tag == 'label':
                uiElement = UIElementUtil.buildLabelElementForSection(child, section)
            elif child.tag == 'nav':
                uiElement = UIElementUtil.buildNavElementForSection(child, section)
            elif child.tag == 'menu':
                uiElement = UIElementUtil.buildMenuElementForSection(child, section)
            elif child.tag == 'menu-input':
                uiElement = UIElementUtil.buildMenuInputElementForSection(child, section)
            section.addElement(uiElement)
            uiElement = None