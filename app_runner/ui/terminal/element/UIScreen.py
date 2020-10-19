import curses
from xml.etree.ElementTree import ElementTree, Element
from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Command import Command
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


class UIScreen(UIElement):
    __views: dict = {}
    __activeViewId: str = None
    __appContext: AppContext
    __colorSet: bool = False

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'screen', appContext)
        self.__appContext = appContext
        self.__setListeners()

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
        currentView = self.getActiveView()
        if currentView is not None:
            currentView.destroy()
        self.__activeViewId = vid
        view = self.getView(vid)
        if view is None:
            view = self.__buildView(vid)
            self.__views[vid] = view
        view.print()

    # Event Handlers

    def executeCommand(self, data: dict):
        print('executeCommand: ' + str(data))

    def commandSelected(self, data: dict):
        cmd: Command = data.get('command')
        if cmd.hasNextMenus():
            EventManager.triggerEvent(UIEventType.DISPLAY_MENUS, {
                'mids': cmd.getMenus()
            })
        else:
            self.displayView('form')

    # Private Methods

    def __setListeners(self):
        EventManager.listenEvent(UIEventType.COMMAND_SELECTED, self)
        EventManager.listenEvent(UIEventType.EXECUTE_COMMAND, self)

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
            elif child.tag == 'menu':
                uiElement = self.__buildMenuElementForSection(child, section)
            elif child.tag == 'form':
                uiElement = self.__buildFormElementForSection(child, section)
            section.addElement(uiElement)

    def __buildFormElementForSection(self, element: Element, section: UISection) -> LabelElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'form')
        form = FormElement(id, self.__appContext)
        form.setParent(section)
        form.setAttributes(element)
        form.setWindow(section.getWindow())
        return form

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

    def __buildMenuElementForSection(self, element: Element, section: UISection) -> MenuElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'menu')
        menu = MenuElement(id, self.__appContext)
        menu.setParent(section)
        menu.setAttributes(element)
        window = section.getDerivedWindow(menu.getX(), menu.getY(), menu.getWidth(), menu.getHeight())
        menu.setWindow(window)
        return menu

    def __setColorsIfNotSet(self):
        if not self.__colorSet:
            UIColor.setColorCodes()
            self.__colorSet = True
