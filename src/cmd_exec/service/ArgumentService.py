import sys
from ..service.AppService import AppService
from ..service.ConfigurationService import ConfigurationService


class ArgumentService(AppService):
    __arguments: dict
    __flags: list
    __configService: ConfigurationService

    def __init__(self, configService: ConfigurationService):
        self.__configService = configService
        self.__arguments = {'mode': 'cmd'}
        self.__setArgumentsAndFlags()
        print("Set")

    # Getter Methods

    def getCmd(self) -> str:
        return self.__arguments.get('cmd')

    def getMode(self) -> str:
        return self.__arguments.get('mode')

    def getArgs(self) -> dict:
        return self.__arguments

    def getArgVal(self, key: str) -> object:
        return self.__arguments.get(key)

    def getFlags(self) -> list:
        if self.__flags is not None:
            return self.__flags
        return None

    def __setArgumentsAndFlags(self):
        args: list = sys.argv[1:]
        param: str = None
        self.__flags = []
        for arg in args:
            if arg.startswith('--'):
                param = arg[2:]
            elif arg.startswith('-'):
                self.__flags += list(arg[1:])
            elif param is not None:
                self.__arguments[param] = arg
            else:
                param = None
