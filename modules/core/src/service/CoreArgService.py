import argparse
import sys

from src.error.CmdExecError import CmdExecError
from src.service.ArgumentService import ArgumentService
from src.service.ConfigService import ConfigService


class CoreArgService(ArgumentService):
    # __argumentParser: argparse.ArgumentParser
    __arguments: dict
    __configService: ConfigService
    # __modes: list
    # __defaultMode: str

    def __init__(self, configService: ConfigService):
        # self.__argumentParser = argparse.ArgumentParser("Provide arguments")
        self.__configService = configService
        self.__arguments = {'mode': 'cmd'}
        self.__setArguments()
        # self.__setModes()
        # self.__setDefaultMode()
        # self.__setDefaultArguments()
        # self.__parseArguments()

    # Getter Methods

    def getCmd(self) -> str:
        return self.__arguments.get('cmd')

    def getMode(self) -> str:
        return self.__arguments.get('mode')

    def getArgs(self) -> dict:
        return self.__arguments

    def __setArguments(self):
        args: list = sys.argv[1:]
        param: str = None
        for arg in args:
            if arg.startswith('-'):
                param = arg[1:]
            elif param is not None:
                self.__arguments[param] = arg
            else:
                param = None

    # def getArgs(self) -> dict:
    #     retArgs: dict = {}
    #     argStr: str = self.__arguments.get('args')
    #     if argStr is not None:
    #         args = argStr.split(',')
    #         for arg in args:
    #             keyValPair = arg.split(':')
    #             retArgs[keyValPair[0]] = keyValPair[1]
    #     return retArgs

    # Private Methods
    #
    # def __setModes(self):
    #     modes: list = self.__configService.getModeIds()
    #     if modes is None or len(modes) == 0:
    #         raise CmdExecError('ERR43')
    #     self.__modes = modes
    #
    # def __setDefaultMode(self):
    #     mode = self.__configService.getDefaultMode()
    #     if mode is None:
    #         mode = self.__modes[0]
    #     self.__defaultMode = mode
    #
    # def __parseArguments(self):
    #     # Parse arguments
    #     args = self.__argumentParser.parse_args()
    #     self.__arguments = vars(args)
    #
    # def __setDefaultArguments(self):
    #     self.__argumentParser.add_argument('--mode', help='Sets program execution mode.', choices=self.__modes, default=self.__defaultMode)
    #     self.__argumentParser.add_argument('--cmd', help='Sets command to execute.')
    #     self.__argumentParser.add_argument('--args', help='Arguments for command in json format.')
