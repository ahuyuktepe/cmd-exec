from src.error.CmdExecError import CmdExecError
from src.module.AppModule import AppModule
from src.util.FileUtil import FileUtil
from src.util.ValidationUtil import ValidationUtil


class ModuleBuilder:

    @staticmethod
    def buildModule(filePath: str) -> AppModule:
        # Parse settings file
        ValidationUtil.failIfFileIsNotReadable(filePath, "Module settings file {path} can not be loaded.", {'path': filePath})
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
        ValidationUtil.failIfStrNoneOrEmpty(name, "Module name is not defined or empty in modules settings file'{path}'.", {'path': filePath})
        # Validate version
        version = props.get('version')
        ValidationUtil.failIfVersionSyntaxInvalid(name, version)
        # Validate dependencies
        dependencies = props.get('dependencies')
        if dependencies is not None and not isinstance(dependencies, list):
            raise CmdExecError("Dependencies are not defined correctly for module '{module}' in file '{path}'.".format(module=name, path=filePath))
