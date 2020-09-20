from xml.etree.ElementTree import ElementTree, Element
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.element.UISection import UISection
from app_runner.ui.terminal.element.UIView import UIView
from app_runner.ui.terminal.utils.UIElementUtil import UIElementUtil
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.FileUtil import FileUtil


class UIScreen:
    __views:  dict = {}
    __activeViewId: str = None

    def __init__(self):
        self.__setListeners()

    def displayView(self, vid: str):
        self.__activeViewId = vid
        view = self.getView(vid)
        if view is None:
            view = self.__buildView(vid)
            self.__views[vid] = view
        view.print()

    # Getter Methods

    def getView(self, vid: str) -> UIView:
        if vid is not None:
            return self.__views.get(vid)

    def getActiveView(self) -> UIView:
        return self.getView(self.__activeViewId)

    def hasActiveView(self) -> bool:
        view = self.getActiveView()
        return view is not None

    # Utility Methods

    def clearView(self):
        view = self.getActiveView()
        if view is not None:
            view.clear()

    def listenUserInput(self):
        view = self.getActiveView()
        if view is not None:
            view.listenUserInput()

    # Event Listeners

    def upKeyPressed(self, data: dict):
        inputElement = self.getActiveView().getInputElement()
        if inputElement is not None:
            inputElement.exitListeningUserInput()
        self.clearView()
        self.displayView('form')
        self.listenUserInput()

    def downKeyPressed(self, data: dict):
        inputElement = self.getActiveView().getInputElement()
        if inputElement is not None:
            inputElement.exitListeningUserInput()
        self.clearView()
        self.displayView('menu')
        self.listenUserInput()

    def leftKeyPressed(self, data: dict):
        inputElement = self.getActiveView().getInputElement()
        if inputElement is not None:
            inputElement.exitListeningUserInput()
        self.clearView()
        self.displayView('test')
        self.listenUserInput()

    # Private Methods

    def __setListeners(self):
        EventManager.bindEvent(UIEventType.UP_KEY_PRESSED, self)
        EventManager.bindEvent(UIEventType.DOWN_KEY_PRESSED, self)
        EventManager.bindEvent(UIEventType.LEFT_KEY_PRESSED, self)

    def __buildView(self, vid: str) -> UIView:
        # Initialize View
        view: UIView = UIView('root')
        view.initialize()
        # Build Object From Xml
        filePath = FileUtil.getAbsolutePath(['resources', 'terminal', 'views', vid])
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
            y += section.getHeight() - 1
            self.__populateSectionElements(element, section)
            screen.addSection(section)

    def __initializeSection(self, element: Element) -> UISection:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        withBorder = XmlElementUtil.isAttrTrue(element, 'border', False)
        section = UISection(id, withBorder)
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
