from threading import Timer

from app_runner.app.context.AppContext import AppContext
from app_runner.services.CommandService import CommandService
from app_runner.classes.KeyboardListenerThread import KeyboardListenerThread
from app_runner.classes.ViewBuilder import ViewBuilder
from app_runner.classes.ViewManager import ViewManager
from app_runner.enums.UIColor import UIColor
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.services.LogService import LogService
from app_runner.services.MenuService import MenuService
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UIView import UIView
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil


class TerminalScreen(UIElement):
    __appContext: AppContext
    __logService: LogService
    __menuService: MenuService
    __viewBuilder: ViewBuilder = None
    __viewManager: ViewManager = None
    __keyboardListener: KeyboardListenerThread = None
    __quit: bool
    __msgTimer: object

    def __init__(self, appContext: AppContext):
        super().__init__('root-screen', 'screen')
        self.__appContext = appContext
        self.__logService = appContext.getService('logService')
        self.__menuService = appContext.getService('menuService')
        menuService = appContext.getService('menuService')
        fieldService = appContext.getService('fieldService')
        self.__viewBuilder = ViewBuilder(menuService, fieldService)
        self.__viewManager = ViewManager()
        self.__quit = False

    # Setter Methods

    def setListeners(self):
        # Set Listener
        EventManager.listenEvent(UIEventType.DISPLAY_VIEW, self)
        EventManager.listenEvent(UIEventType.QUIT_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.COMMAND_SELECTED, self)
        EventManager.listenEvent(UIEventType.RETURN_TO_MENU_VIEW, self)

    # Utility Methods

    def setup(self):
        # Setup Print Area
        UIPrintAreaUtil.initializeScreen()
        self._printArea = UIPrintAreaUtil.buildScreenPrintArea()
        # Setup Colors
        UIColor.setColorCodes()
        # Set Listeners
        self.setListeners()
        # Listen Keyboard
        self.__keyboardListener = KeyboardListenerThread(self._printArea, self.__logService)

    def start(self):
        self.displayView({'vid': 'menu'})
        self.__keyboardListener.listen()

    def displayMessage(self, text: str):
        EventManager.triggerEventByElementId(UIEventType.UPDATE_TEXT, 'msg-box', {
            'text': text
        })
        self.__msgTimer = Timer(5, self.clearMessage)
        self.__msgTimer.start()

    def clearMessage(self):
        EventManager.triggerEventByElementId(UIEventType.UPDATE_TEXT, 'msg-box', {'text': ''})
        self.__msgTimer.cancel()

    # Event Listeners

    def returnToMenuView(self, data):
        self.displayView({'vid': 'menu'})

    def commandSelected(self, data):
        cmd = data.get('command')
        if cmd.hasNextMenus():
            mids = cmd.getMenus()
            menus = self.__menuService.buildMenus(mids)
            EventManager.triggerEvent(UIEventType.DISPLAY_MENUS, {
                'parentMenuName': cmd.getDescription(),
                'menus': menus
            })
        elif cmd.hasFields():
            # Collect Parameter Values
            self.__viewManager.closeActiveView()
            self.displayView({'vid': 'form'})
        elif cmd.hasExecutor():
            # Set Command Executor Thread
            cmdService: CommandService = self.__appContext.getService('commandService')
            cmdService.execute(cmd, {})
        else:
            self.displayMessage("Given command '" + cmd.getDescription() + "' does not have executor.")

    def quitKeyPressed(self, data):
        self.__quit = True

    def displayView(self, data: dict = {}):
        vid: str = data.get('vid')
        view: UIView = self.__viewManager.getView(vid)
        if view is None:
            view = self.__viewBuilder.buildView(self.getPrintArea(), vid, data)
        self.__viewManager.addAndActivateView(view)
        view.display()
        self.setListeners()
