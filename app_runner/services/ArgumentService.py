import argparse
from app_runner.services.BaseService import BaseService
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.StrUtil import StrUtil

class ArgumentService(BaseService):
    argumentParser: argparse.ArgumentParser = argparse.ArgumentParser("Provide arguments")
    __arguments: dict = None

    def __init__(self):
        self.__setDefaultArguments()
        self.__parseArguments()

    # Getter Methods

    def getCmd(self) -> str:
        return self.__arguments.get('cmd')

    def getMenu(self) -> str:
        if self.isCmdMode():
            cmd: str = self.__arguments.get('cmd')
            arr = cmd.split('.')
            count = len(arr)
            if count == 2:
                return arr[0]
            elif count == 1:
                return 'core'
        return None

    def getArgsFileName(self) -> str:
        return self.__arguments.get('args_file')

    def getArgAsStr(self) -> str:
        return self.__arguments.get('args_str')

    def getArgsAsDict(self, cid: str) -> dict:
        retDict: dict = {}
        args: dict = {}
        if self.__areArgsFromCmdParam():
            argStr: str = self.getArgAsStr()
            args = StrUtil.getObjFromArgsStr(argStr)
        elif self.__areArgsFromFile():
            filePath: str = FileUtil.getAbsolutePath(['resources', 'args', self.getArgsFileName()])
            ext: str = FileUtil.getFileExtension(filePath)
            if ext == 'json':
                args = FileUtil.generateObjFromJsonFile(filePath)
            elif ext == 'yaml':
                args = FileUtil.generateObjFromYamlFile(filePath)
        # ObjUtil.mergeDictIntoOther(args, retDict)
        retDict.update(args)
        return retDict

    # Query Methods

    def isInteractiveMode(self) -> bool:
        mode: str = self.__arguments.get('mode')
        return mode == 'int'

    def isCmdMode(self) -> bool:
        mode: str = self.__arguments.get('mode')
        return mode == 'cmd'

    # Private Methods

    def __parseArguments(self):
        # Parse arguments
        args = self.argumentParser.parse_args()
        self.__arguments = vars(args)

    def __setDefaultArguments(self):
        # Setup argument parser
        self.argumentParser.add_argument('--mode',
                                         help='Sets program execution mode.',
                                         choices=['int', 'cmd'],
                                         default='int')
        self.argumentParser.add_argument('--cmd',
                                         help='Sets command to execute.')
        self.argumentParser.add_argument('--args_str',
                                         help='Sets arguments to passed while executing command.')
        self.argumentParser.add_argument('--args_file',
                                         help='Sets file path to json file which contains arguments '
                                              'to be used while executing command.')

    def __areArgsFromCmdParam(self) -> bool:
        return self.getArgAsStr() is not None

    def __areArgsFromFile(self) -> bool:
        return self.getArgsFileName() is not None
