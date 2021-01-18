import os
from src.error.CmdExecError import CmdExecError
from src.util.FileUtil import FileUtil
from src.util.ListUtil import ListUtil
from src.util.StrUtil import StrUtil
from src.util.ValidationUtil import ValidationUtil


class ModuleUtil:

    @staticmethod
    def getModuleNames() -> list:
        modulesDirPath = FileUtil.getAbsolutePath(['modules'])
        directories = os.listdir(modulesDirPath, )
        ListUtil.deleteElements(directories, ['__pycache__'])
        return directories

    @staticmethod
    def validateModuleDirectoryAndFiles(name: str):
        path = ['modules']
        modulesPath = FileUtil.getAbsolutePath(path)
        # Validate Root Directory
        path.append(name)
        ValidationUtil.failIfDirectoryCanNotBeAccessed(path, 'ERR19', {'name': name, 'path': modulesPath})
        # Validate Settings File
        path.append(name + '.settings.yaml')
        settingsFilePath = FileUtil.getAbsolutePath(path)
        ValidationUtil.failIfFileCanNotBeAccessed(path, 'ERR06',  {'name': name, 'path': settingsFilePath})

    @staticmethod
    def validateModuleProperties(moduleName: str, props: dict):
        # Validate name property
        nameProp = props.get('name')
        ValidationUtil.failIfStrNoneOrEmpty(nameProp, 'ERR01', {'module': moduleName})
        if moduleName != nameProp:
            raise CmdExecError('ERR20', {'name': nameProp})
        # Validate version
        version = props.get('version')
        if StrUtil.isVersionSyntaxInvalid(version):
            raise CmdExecError('ERR02', {'version': version, 'module': moduleName})
        # Validate dependencies
        dependencies = props.get('dependencies')
        if dependencies is not None and not isinstance(dependencies, list):
            raise CmdExecError('ERR03', {'module': moduleName})

    @staticmethod
    def getModuleSettings(name: str) -> dict:
        settingsFileName = name + '.settings.yaml'
        return FileUtil.generateObjFromYamlFile(['modules', name, settingsFileName])

    # ==================================================================================================================

    # @staticmethod
    # def getConfigFilePaths() -> list:
    #     modulesDirPath = FileUtil.getAbsolutePath(['modules'])
    #     filePattern = "{modulesDirPath}/*/*.config.yaml".format(modulesDirPath=modulesDirPath)
    #     return glob.glob(filePattern)

    # @staticmethod
    # def getSettingFilePaths() -> list:
    #     modulesDirPath = FileUtil.getAbsolutePath(['modules'])
    #     filePattern = "{modulesDirPath}/*/*.settings.yaml".format(modulesDirPath=modulesDirPath)
    #     return glob.glob(filePattern)
