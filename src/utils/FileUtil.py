import os
import yaml
from src.errors.CmdExecError import CmdExecError


class FileUtil:
    @staticmethod
    def getAbsolutePath(path: list) -> str:
        return os.environ['APP_RUNNER_ROOT_PATH'] + os.path.sep + os.path.sep.join(path)

    @staticmethod
    def generateObjFromYamlFile(path: str) -> object:
        try:
            stream = open(path, 'r')
            retObj = yaml.load(stream, Loader=yaml.SafeLoader)
            return retObj
        except Exception as exp:
            msg = "Error occurred while parsing xml file '{path}'.".format(path=path)
            raise CmdExecError(msg)
