from src.error.CmdExecError import CmdExecError
from src.util.ListUtil import ListUtil
from src.util.StrUtil import StrUtil


class ModuleDependency:
    __name: str
    __operator: str
    __version: str

    def __init__(self, depStr: str):
        values = depStr.split('|')
        self.__name = ListUtil.getByIndex(values, 0)
        self.__operator = ListUtil.getByIndex(values, 1)
        self.__version = ListUtil.getByIndex(values, 2)
        self.__validateDependencyStr(depStr)

    # Getter Methods

    def getModuleName(self) -> str:
        return self.__name

    def hasNoVersion(self) -> bool:
        return self.__operator is None

    # Utility Methods

    def validate(self, dependingModName: str, trgVersion: str = None, doesTrgModVersionExist: bool = False):
        filledDepModVersion = StrUtil.prefillVersion(self.__version)
        filledTrgModVersion = StrUtil.prefillVersion(trgVersion)
        if self.hasNoVersion() and not doesTrgModVersionExist:
            msg = "Module '{srcModule}' depends on module '{depModule}' but not found."
            raise CmdExecError(msg.format(srcModule=dependingModName, depModule=self.__name))
        elif self.__operator == '=' and filledDepModVersion != filledTrgModVersion:
            msg = "Module '{srcModule}' depends on module '{depModule}' with version '{depVersion}' but version '{trgVersion}' found."
            raise CmdExecError(msg.format(srcModule=dependingModName, depModule=self.__name, depVersion=self.__version, trgVersion=trgVersion))
        elif self.__operator == '>' and filledTrgModVersion <= filledDepModVersion:
            msg = "Module '{srcModule}' depends on module '{depModule}' with version  greater then '{depVersion}' but found '{trgVersion}'."
            raise CmdExecError(msg.format(srcModule=dependingModName, depModule=self.__name, depVersion=self.__version, trgVersion=trgVersion))
        elif self.__operator == '<' and filledTrgModVersion >= filledDepModVersion:
            msg = "Module '{srcModule}' depends on module '{depModule}' with version less then '{depVersion}' but found '{trgVersion}'."
            raise CmdExecError(msg.format(srcModule=dependingModName, depModule=self.__name, depVersion=self.__version, trgVersion=trgVersion))
        elif self.__operator == '<=' and filledTrgModVersion > filledDepModVersion:
            msg = "Module '{srcModule}' depends on module '{depModule}' with version less then or equal to '{depVersion}' but found '{trgVersion}'."
            raise CmdExecError(msg.format(srcModule=dependingModName, depModule=self.__name, depVersion=self.__version, trgVersion=trgVersion))
        elif self.__operator == '>=' and filledTrgModVersion < filledDepModVersion:
            msg = "Module '{srcModule}' depends on module '{depModule}' with version greater then or equal to '{depVersion}' but found '{trgVersion}'."
            raise CmdExecError(msg.format(srcModule=dependingModName, depModule=self.__name, depVersion=self.__version, trgVersion=trgVersion))

    # Private Methods

    def __validateDependencyStr(self, depStr: str):
        if depStr is None:
            raise CmdExecError('Given dependency identifier is null.')
        values = depStr.split('|')
        if len(values) == 1:
            return
        if len(values) == 2:
            raise CmdExecError("Given dependency identifier '{id}' contains missing information.".format(id=depStr))
        elif len(values) > 3:
            raise CmdExecError("Given dependency identifier '{id}' contains redundant information.".format(id=depStr))
        elif values[1] not in ['=', '<', '>', '>=', '<=']:
            raise CmdExecError("Given dependency identifier '{id}' contains invalid operator.".format(id=depStr))
        elif StrUtil.isVersionSyntaxInvalid(values[2]):
            raise CmdExecError("Dependency module '{depModule}' version '{version}' is not valid for module '{module}'.".format(
                depModule=values[0],
                version=values[2],
                module=self.__name
            ))
