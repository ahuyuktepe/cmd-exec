from xml.etree.ElementTree import ElementTree, Element

from app_runner.app.context.AppContext import AppContext
from app_runner.ui.terminal.element.FormElement import FormElement
from app_runner.ui.terminal.element.LabelElement import LabelElement
from app_runner.ui.terminal.element.MenuElement import MenuElement
from app_runner.ui.terminal.element.MenuInputElement import MenuInputElement
from app_runner.ui.terminal.element.MessageElement import MessageElement
from app_runner.ui.terminal.element.NavElement import NavElement
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.element.UISection import UISection
from app_runner.ui.terminal.element.UIView import UIView
from app_runner.ui.terminal.enums.UIColor import UIColor
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.FileUtil import FileUtil
import time


class UIScreen:
    __views: dict = {}
    __activeViewId: str = None
    __appContext: AppContext
    __colorSet: bool = False

    def __init__(self, appContext: AppContext):
        self.__appContext = appContext

    # Getter Methods

    def getView(self, vid: str) -> UIView:
        return self.__views.get(vid)

    def getActiveView(self) -> UIView:
        return self.getView(self.__activeViewId)

    def hasActiveView(self) -> bool:
        view = self.getActiveView()
        return view is not None

    # Utility Methods

    def displayView(self, vid: str):
        self.__activeViewId = vid
        view = self.getView(vid)
        if view is None:
            view = self.__buildView(vid)
            self.__views[vid] = view
        view.print()

    # Private Methods

    def __buildView(self, vid: str) -> UIView:
        # Build Object From Xml
        filePath = FileUtil.getAbsolutePath(['resources', 'terminal', 'views', vid])
        elementTree: ElementTree = FileUtil.generateObjFromFile(filePath + '.xml')
        root: Element = elementTree.getroot()
        # Initialize View
        id = XmlElementUtil.getAttrValueAsStr(root, 'id', None)
        view: UIView = UIView(id, self.__appContext)
        view.initialize()
        self.__setColorsIfNotSet()
        view.setAttributes(root)
        # Populate Sections
        self.__populateSectionsFromXml(root, view)
        return view

    def __populateSectionsFromXml(self, root: Element, screen: UIView):
        sections = root.findall('./section')
        y = 0
        for element in sections:
            section: UISection = self.__initializeSection(element)
            section.setParent(screen)
            section.setAttributes(element)
            section.setY(y)
            section.initialize()
            y += section.getHeight() - 1
            self.__populateSectionElements(element, section)
            screen.addSection(section)

    def __initializeSection(self, element: Element) -> UISection:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        section = UISection(id, self.__appContext)
        return section

    def __populateSectionElements(self, element: Element, section: UISection):
        uiElement: UIElement = None
        for child in element:
            if child.tag == 'label':
                uiElement = self.__buildLabelElementForSection(child, section)
            elif child.tag == 'menu-input':
                uiElement = self.__buildMenuInputElementForSection(child, section)
            elif child.tag == 'message':
                 uiElement = self.__buildMessageElementForSection(child, section)
            elif child.tag == 'nav':
                uiElement = self.__buildNavElementForSection(child, section)
            section.addElement(uiElement)

    def __buildLabelElementForSection(self, element: Element, section: UISection) -> LabelElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'lbl')
        label = LabelElement(id, self.__appContext)
        label.setParent(section)
        label.setAttributes(element)
        label.setWindow(section.getWindow())
        return label

    def __buildMessageElementForSection(self, element: Element, section: UISection) -> MessageElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'msg')
        msg = MessageElement(id, self.__appContext)
        msg.setParent(section)
        msg.setAttributes(element)
        msg.setWindow(section.getWindow())
        return msg

    def __buildNavElementForSection(self, element: Element, section: UISection) -> NavElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'nav')
        nav = NavElement(id, self.__appContext)
        nav.setParent(section)
        nav.setAttributes(element)
        nav.setWindow(section.getWindow())
        return nav

    def __buildMenuInputElementForSection(self, element: Element, section: UISection) -> MenuInputElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'menu-input')
        input = MenuInputElement(id, self.__appContext)
        input.setParent(section)
        input.setAttributes(element)
        input.setWindow(section.getWindow())
        return input

    def __setColorsIfNotSet(self):
        if not self.__colorSet:
            UIColor.setColorCodes()
            self.__colorSet = True
