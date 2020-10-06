from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.element.UIElement import UIElement


class MenuElement(UIElement):
    __menu: Menu
    __activeIndex: int

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'menu', appContext)
        self.__menu = None
        self.__activeIndex = 0

    # Setter Methods

    def setAttributes(self, element: Element):
        pass
