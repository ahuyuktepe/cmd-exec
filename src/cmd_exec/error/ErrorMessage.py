class ErrorMessage:
    messages: dict = {
        'ERR01': "Module name is not defined or empty for module '{module}'.",
        'ERR02': "Invalid version '{version}' provided for module '{module}'.",
        'ERR03': "Dependencies are not defined correctly for module '{module}'.",
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
        'ERR28': "Given service class '{src}' is not sub class of 'AppService'.",
        'ERR29': "Invalid value '{val}' is provided for init property in settings file for module '{name}'.Boolean value True|False is expected.",
        'ERR30': "Service class '{cls}' file does not exist at '{path}'.",
        'ERR31': "Command executor application class '{cls}' file does not exist at '{path}'.",
        'ERR32': "Given class '{src}' is not sub class of '{parent}' in module '{name}' configs.",
        'ERR33': "None value provided for module property of executor '{executor}' in command file {file}.",
        'ERR34': "Command file '{file}' does not exist in commands directory located in either module or resources directory.",
        'ERR35': "Invalid id provided in command file '{cid}.yaml'.",
        'ERR36': "Invalid title provided in command file '{cid}.yaml'.",
        'ERR37': "Invalid executor provided in command file '{cid}.yaml'.",
        'ERR38': "Invalid class provided for executor in command file '{cid}.yaml'.",
        'ERR39': "Invalid method provided for executor in command file '{cid}.yaml'.",
        'ERR40': "Given executor class in command file '{cid}.yaml' does not extend from ..CmdExecutor.",
        'ERR41': "Invalid module provided in command file '{cid}.yaml'.",
        'ERR42': "Invalid value provided for application.default_mode property in configurations.",
        'ERR43': "At least one application running mode should be provided in configurations.",
        'ERR44': "Invalid value provided for application.modes property in configurations.",
        'ERR45': "Invalid value provided for fields property in configurations.",
        'ERR46': "Invalid values provided for field properties in configurations.",
        'ERR47': "Invalid value provided for class property of field type '{type}' in configurations.",
        'ERR48': "Invalid value provided for module property of field type '{type}' in configurations.",
        'ERR49': "Field class does not exist in path '{path}'.",
        'ERR50': "No class properties are provided for field type '{type}'.",
        'ERR51': "Executor class does not exist in path '{path}'.",
        'ERR52': "Field validation failed.",
        'ERR53': "Invalid field type '{type}' is given for command '{cid}'.",
        'ERR54': "Field property {property} for command '{cid}' is either null or empty.",
        'ERR55': "Invalid value is provided for field '{fid}' property '{prop}'.",
        'ERR56': "Given value '{value}' for date field '{fid}' is not in allowable date range '{from}' - '{to}'.",
        'ERR57': "Field '{fid}' is required but no value provided.",
        'ERR58': "File '{path}' for field '{fid}' does not exist.",
        'ERR59': "Given executor class does not extend from ..CmdExecuter lass.",
        'ERR60': "None or empty value is given for cmd.",
        'ERR61': "Given value '{value}' size for field '{fid}' is less then min_size value '{min_size}'",
        'ERR62': "Given value '{value}' size for field '{fid}' is greater then max_size value '{max_size}'",
        'ERR63': "Invalid configuration key '{key}' is given.",
        'ERR64': "Existing config value '{existingVal}' type and new value '{newVal}' type does not match.",
        'ERR65': "Invalid default options provided for field '{fid}'.",
        'ERR67': "For field '{fid}' at least {min} option(s) should be selected.",
        'ERR68': "For field '{fid}' less then {max} option(s) should be selected.",
        'ERR69': "No option is provided for selection field '{fid}'.",
        'ERR70': "Invalid properties provided for application.actions.before_command configuration.",
        'ERR71': "Given action class does not extend from ..CmdAction class.",
        'ERR72': "Given command action response is not type of CmdActionResponse.",
        'ERR73': "Pre command action failed. Details: {details}",
        'ERR74': "Invalid properties provided for application.actions.after_command configuration.",
        'ERR75': "Post command action failed. Details: {details}",
        'ERR76': "File does not exist in {path}.",
        'ERR77': "Primary key for domain object is not set.",
        'ERR78': "User '{user}' is not in allowed users {users} to run command '{cmd}'.",
        'ERR79': "User '{user}' is in denied users {users} to run command '{cmd}'.",
        'ERR80': "User '{user}' is not assigned to any allowed group {groups} to run command '{cmd}'.",
        'ERR81': "User '{user}' is assigned to a group in denied groups {groups} to run command '{cmd}'."
    }

    @staticmethod
    def getMessage(code: str) -> str:
        return ErrorMessage.messages[code]
