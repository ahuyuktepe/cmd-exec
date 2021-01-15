class ErrorMessage:
    messages: dict = {
        'ERR01': "Module name is not defined or empty in modules settings file '{path}'.",
        'ERR02': "Invalid version '{version}' provided for module '{module}'.",
        'ERR03': "Dependencies are not defined correctly for module '{module}' in file '{path}'.",
        'ERRO4': "Environment variable '{name}' is not set.",
        'ERR05': "Config file {path} can not be loaded.",
        'ERR06': "Module settings file {path} can not be loaded.",
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
        'ERR18': "Configuration key '{key}' contains unsupported character ':' in configuration file '{path}'."
    }

    @staticmethod
    def getMessage(code: str) -> str:
        return ErrorMessage.messages[code]
