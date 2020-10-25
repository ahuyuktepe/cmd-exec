from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Menu import Menu
from app_runner.services.MenuService import MenuService
from app_runner.ui.terminal.element.UIScreen import UIScreen


class IntAppRunner(ApplicationRunner):
    __screen: UIScreen

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__screen = UIScreen('screen', context)

    def run(self):
        self.__screen.displayView('form')
        menuService: MenuService = self._appContext.getService('menuService')
        menu: Menu = menuService.buildMenu('main')
        cmd = menu.getCommand('cpy')
        EventManager.triggerEvent(UIEventType.COLLECT_FIELD_VALUES, {
            'command': cmd
        })
