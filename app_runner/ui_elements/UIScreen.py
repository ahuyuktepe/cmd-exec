from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Command import Command
from app_runner.services.FieldService import FieldService
from app_runner.services.MenuService import MenuService
from app_runner.classes.ViewManager import ViewManager
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UIView import UIView


class UIScreen(UIElement):
    __appContext: AppContext
    __menuService: MenuService
    __fieldService: FieldService
    __viewManager: ViewManager
    __selectedCmd: Command
    __collectedFieldValues: dict

    def __init__(self, appContext: AppContext):
        super().__init__('root-screen', 'screen')
        self.__appContext = appContext
        self.__menuService = appContext.getService('menuService')
        self.__fieldService = appContext.getService('fieldService')
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
        self.__selectedCmd = None
        self.displayView('menu', data)
        return self.__selectedCmd

    def collectFieldValues(self, cmd: Command) -> dict:
        self.displayView('form', {
            'command': cmd
        })
        EventManager.triggerEvent(UIEventType.COLLECT_FIELD_VALUES)
        return self.__collectedFieldValues

    def displayXml(self, html: str):
        self.displayView('html')
        EventManager.triggerEvent(UIEventType.DISPLAY_XML, {
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
