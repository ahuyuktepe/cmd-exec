class ErrorMessage:
    messages: dict = {
        'ERR01': "Module name is not defined or empty for module '{module}'.",
        'ERR02': "Invalid version '{version}' provided for module '{module}'.",
        'ERR03': "Dependencies are not defined correctly for module '{module}'.",
        'ERRO4': "Environment variable '{name}' is not set.",
        'ERR05': "Configuration file '{file}' for module '{name}' can not be loaded.",
        'ERR06': "Settings file does not exist or can not be read for module '{name}' located in '{path}'.",
        'ERR07': "Module '{srcModule}' depends on module '{depModule}' but not found.",
        'ERR08': "Module '{srcModule}' depends on module '{depModule}' with version '{depVersion}' but version '{trgVersion}' found.",
        'ERR09': "Module '{srcModule}' depends on module '{depModule}' with version  greater then '{depVersion}' but found '{trgVersion}'.",
        'ERR10': "Module '{srcModule}' depends on module '{depModule}' with version less then '{depVersion}' but found '{trgVersion}'.",
        'ERR11': "Module '{srcModule}' depends on module '{depModule}' with version less then or equal to '{depVersion}' but found '{trgVersion}'.",
        'ERR12': "Module '{srcModule}' depends on module '{depModule}' with version greater then or equal to '{depVersion}' but found '{trgVersion}'.",
        'ERR13': "Given dependency identifier is null.",
        'ERR14': "Given dependency identifier '{id}' contains missing information.",
        'ERR15': "Given dependency identifier '{id}' contains redundant information.",
        'ERR16': "Given dependency identifier '{id}' contains invalid operator.",
        'ERR17': "Dependency module '{depModule}' version '{version}' is not valid for module '{module}'.",
        'ERR18': "Configuration key '{key}' contains unsupported character '.' in configuration file for module '{name}'.",
        'ERR19': "Directory does not exist or is not accessible for module '{name}' in '{path}'.",
        'ERR20': "Provided module name '{name}' in setting file does not match with module directory and settings file prefix.",
        'ERR21': "Directories '{dirs}' in command executor home directory '{home}' can not be deleted.",
        'ERR22': "Given yaml file '{path}' does not have validate content",
        'ERR23': "Empty or none value provided for service {type} in settings file or module '{name}'.",
        'ERR24': "Invalid value is provided for services property in settings file of module '{name}'.",
        'ERR25': "Invalid service path '{path}' provided.",
        'ERR26': "Null value is provided to save service for id '{sid}'.",
        'ERR27': "While initializing service null service properties object provided.",
        'ERR28': "Given service object class '{cls}' is not sub class of 'AppService'",
        'ERR29': "Invalid value '{val}' is provided for init property in settings file for module '{name}'.Boolean value True|False is expected."
    }

    @staticmethod
    def getMessage(code: str) -> str:
        return ErrorMessage.messages[code]
