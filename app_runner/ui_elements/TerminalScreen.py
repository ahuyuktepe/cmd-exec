from app_runner.app.context.AppContext import AppContext
from app_runner.builders.PrintAreaBuilder import PrintAreaBuilder
from app_runner.classes.KeyboardListener import KeyboardListener
from app_runner.builders.ViewBuilder import ViewBuilder
from app_runner.classes.ViewManager import ViewManager
from app_runner.enums.UIColor import UIColor
from app_runner.events.EventManager import EventManager
from app_runner.events.FlowEventType import FlowEventType
from app_runner.services.LogService import LogService
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UIView import UIView


class TerminalScreen(UIElement):
    __appContext: AppContext
    __logService: LogService
    __viewBuilder: ViewBuilder = None
    __viewManager: ViewManager = None
    __printAreaBuilder: PrintAreaBuilder = None
    __keyboardListener: KeyboardListener = None

    def __init__(self, appContext: AppContext, viewBuilder: ViewBuilder, printAreaBuilder: PrintAreaBuilder):
        super().__init__('root-screen', 'screen')
        self.__appContext = appContext
        self.__viewBuilder = viewBuilder
        self.__viewManager = ViewManager()
        self.__printAreaBuilder = printAreaBuilder
        self.__logService = appContext.getService('logService')
        self.__quit = False

    # Flow Methods

    def listenEvents(self):
        # Set Listener
        EventManager.listenEvent(FlowEventType.DISPLAY_VIEW, self)
        EventManager.listenEvent(FlowEventType.COMMAND_SELECTED, self)

    def setup(self):
        # Setup Print Area
        self.__printAreaBuilder.initialize()
        self._printArea = self.__printAreaBuilder.buildPrintAreaForFullScreen()
        # Setup Colors
        UIColor.setColorCodes()
        # Set Listeners
        self.listenEvents()
        # Listen Keyboard
        self.__keyboardListener = KeyboardListener(self._printArea, self.__logService)
        self.__keyboardListener.listen()

    def displayView(self, data: dict):
        # Build View
        vid: str = data.get('vid')
        view: UIView = self.__viewManager.getView(vid)
        if view is None:
            view = self.__viewBuilder.buildView(self.getPrintArea(), vid)
            self.__viewManager.addView(view)
        # Display View
        self.__viewManager.activateView(view)
        view.display()
        # Setup View
        self.listenEvents()

    # ============= Code To Be Enabled ==============

    # def displayMessage(self, text: str):
    #     EventManager.triggerEventByElementId(FlowEventType.UPDATE_TEXT, 'msg-box', {
    #         'text': text
    #     })
    #     self.__msgTimer = Timer(5, self.clearMessage)
    #     self.__msgTimer.start()

    # def clearMessage(self):
    #     EventManager.triggerEventByElementId(FlowEventType.UPDATE_TEXT, 'msg-box', {'text': ''})
    #     self.__msgTimer.cancel()

    # def getForm(self) -> UIForm:
    #     view: UIView = self.__viewManager.getActiveView()
    #     form = view.getFirstElementByType('form')
    #     return form

    # def getCommandArguments(self, cmd: Command) -> dict:
    #     form: UIForm = self.getForm()
    #     args = form.getCommandArguments(cmd)

    # def returnToMenuView(self, data):
    #     self.displayView({'vid': 'menu'})

    # def commandSelected(self, data):
    #     # Set Command Executor Thread
    #     cmdService: CommandService = self.__appContext.getService('commandService')
    #     cmd = data.get('command')
    #     if cmd.hasNextMenus():
    #         mids = cmd.getMenus()
    #         menus = self.__menuService.buildMenus(mids)
    #         EventManager.triggerEvent(FlowEventType.DISPLAY_MENUS, {
    #             'parentMenuName': cmd.getDescription(),
    #             'menus': menus
    #         })
    #     elif cmd.hasFields():
    #         # Collect Parameter Values
    #         self.__viewManager.closeActiveView()
    #         self.displayView({'vid': 'form'})
    #         args = self.getCommandArguments(cmd)
    #         cmdService.execute(cmd, args)
    #     elif cmd.hasExecutor():
    #         cmdService.execute(cmd, {})
    #     else:
    #         self.displayMessage("Given command '" + cmd.getDescription() + "' does not have executor.")