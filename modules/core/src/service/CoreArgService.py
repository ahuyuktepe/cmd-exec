import argparse
from src.service.ArgumentService import ArgumentService
from src.service.ConfigService import ConfigService


class CoreArgService(ArgumentService):
    __argumentParser: argparse.ArgumentParser = argparse.ArgumentParser("Provide arguments")
    __arguments: dict = None
    __configService: ConfigService
    __modes: list

    def __init__(self, configService: ConfigService):
        self.__configService = configService
        self.__modes = self.__configService.getModeIds()
        self.__setDefaultArguments()
        self.__parseArguments()

    # Getter Methods

    def getCmd(self) -> str:
        return self.__arguments.get('cmd')

    def getMode(self) -> str:
        return self.__arguments.get('mode')

    # Private Methods

    def __parseArguments(self):
        # Parse arguments
        args = self.__argumentParser.parse_args()
        self.__arguments = vars(args)

    def __setDefaultArguments(self):
        self.__argumentParser.add_argument('--mode', help='Sets program execution mode.', choices=self.__modes, default='cmd')
        self.__argumentParser.add_argument('--cmd', help='Sets command to execute.')
