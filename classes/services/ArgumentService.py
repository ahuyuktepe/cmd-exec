import argparse

class ArgumentService:
    argumentParser: argparse.ArgumentParser = argparse.ArgumentParser("Provide arguments")
    __arguments: dict = None

    def __init__(self):
        self.__setDefaultArguments()
        self.__parseArguments()

    def __parseArguments(self):
        # Parse arguments
        args = self.argumentParser.parse_args()
        self.__arguments = vars(args)

    def __setDefaultArguments(self):
        # Setup argument parser
        self.argumentParser.add_argument('--mode',
                                         help='Sets program execution mode.',
                                         choices=['interactive', 'cmd'],
                                         default=0)
        self.argumentParser.add_argument('--cmd',
                                         help='Sets command to execute.')
        self.argumentParser.add_argument('--args',
                                         help='Sets arguments to passed while executing command.')
        self.argumentParser.add_argument('--file',
                                         help='Sets file path to json file which contains arguments '
                                              'to be used while executing command.')
        self.argumentParser.add_argument('--menu',
                                         help='Set menu id from which command will be executed.')

    def isInteractiveMode(self) -> bool:
        mode: str = self.__arguments.get('mode')
        return mode == 0 or mode == 'interactive'

    def isCmdMode(self) -> bool:
        mode: str = self.__arguments.get('mode')
        return mode == 'cmd'

    def getFileName(self) -> str:
        return self.__arguments.get('file')

    def getCommand(self) -> str:
        return self.__arguments.get('cmd')

    def getMenu(self) -> str:
        menu: str = self.__arguments.get('menu')
        if menu:
            return menu
        return 'main'

    def getCommandArguments(self):
        return self.__arguments.get('args')

    def getPassedArgumentsAsStr(self):
        return str(self.__arguments)
