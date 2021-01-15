from src.error.CmdExecError import CmdExecError
from src.module.AppModule import AppModule
from src.util.FileUtil import FileUtil
from src.util.StrUtil import StrUtil
from src.util.ValidationUtil import ValidationUtil


class ModuleBuilder:

    @staticmethod
    def buildModule(filePath: str) -> AppModule:
        # Parse settings file
        ValidationUtil.failIfFileIsNotReadable(filePath, 'ERR06', {'path': filePath})
        props = FileUtil.generateObjFromYamlFile(filePath)
        ModuleBuilder.__validateModuleProperties(props, filePath)
        module = AppModule(props['name'], props['version'])
        # Build dependencies
        dependencies = props.get('dependencies')
        if dependencies is not None:
            for dependency in dependencies:
                module.addDependency(dependency)
        return module

    @staticmethod
    def __validateModuleProperties(props: dict, filePath: str):
        # Validate name
        name = props.get('name')
        ValidationUtil.failIfStrNoneOrEmpty(name, 'ERR01', {'path': filePath})
        # Validate version
        version = props.get('version')
        if StrUtil.isVersionSyntaxInvalid(version):
            raise CmdExecError('ERR02', {'version': version, 'module': name})
        # Validate dependencies
        dependencies = props.get('dependencies')
        if dependencies is not None and not isinstance(dependencies, list):
            raise CmdExecError('ERR03', {'module': name, 'path': filePath})
