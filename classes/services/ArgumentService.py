import argparse

from classes.utils.FileUtil import FileUtil
from classes.utils.StrUtil import StrUtil


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
                                         choices=['int', 'cmd'],
                                         default=0)
        self.argumentParser.add_argument('--cid',
                                         help='Sets command to execute.')
        self.argumentParser.add_argument('--args_str',
                                         help='Sets arguments to passed while executing command.')
        self.argumentParser.add_argument('--args_file',
                                         help='Sets file path to json file which contains arguments '
                                              'to be used while executing command.')
        self.argumentParser.add_argument('--mid',
                                         help='Set menu id from which command will be executed.')

    def isInteractiveMode(self) -> bool:
        mode: str = self.__arguments.get('mode')
        return mode == 0 or mode == 'int'

    def isCmdMode(self) -> bool:
        mode: str = self.__arguments.get('mode')
        return mode == 'cmd'

    def getCmdId(self) -> str:
        return self.__arguments.get('cid')

    def getMenuId(self) -> str:
        menu: str = self.__arguments.get('mid')
        if menu:
            return menu
        return 'main'

    def getArgsFileName(self) -> str:
        return self.__arguments.get('args_file')

    def getArgAsStr(self):
        return self.__arguments.get('args_str')

    def areArgsFromCmdParam(self):
        return self.getArgAsStr() is not None

    def areArgsFromFile(self):
        return self.getArgsFileName() is not None

    def getArgsAsDict(self):
        if self.areArgsFromCmdParam():
            argStr: str = self.getArgAsStr()
            return StrUtil.getObjFromArgsStr(argStr)
        elif self.areArgsFromFile():
            filePath = 'temp/' + self.getArgsFileName()
            return FileUtil.generateObjFromJsonFile(filePath)
