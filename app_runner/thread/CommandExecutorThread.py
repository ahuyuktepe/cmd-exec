import threading
from app_runner.menu.Command import Command
from app_runner.services.CommandService import CommandService


class CommandExecutorThread:
    __thread: object = None
    __cmdService: CommandService

    def __init__(self, cmdService: CommandService):
        self.__cmdService = cmdService
        self.__isRunning = False

    def executeCommand(self, cmd: Command):
        if self.__thread is None:
            # Listen Keyboard
            self.__thread = threading.Thread(target=self.__executeCommandInThread, args=(cmd,))
            self.__thread.start()

    def __executeCommandInThread(self, cmd: Command):
        self.__cmdService.execute(cmd, {})
