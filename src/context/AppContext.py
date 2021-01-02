from src.config.AppConfig import AppConfig
from src.utils.FileUtil import FileUtil
from src.utils.StrUtil import StrUtil
from src.utils.ValidationUtil import ValidationUtil


class AppContext:
    __configs: dict

    def __init__(self):
        self.__configs = {}

    # Utility Methods

    def initializeConfig(self, name: str):
        if name is not None:
            props = StrUtil.getFilePropertiesFromStr(name)
            # Parse Config Name
            mid = props.get('module')
            fileName = props.get('file')
            filePath = FileUtil.getAbsolutePath(['modules', mid, 'conf', fileName]) + '.yaml'
            configProps = FileUtil.generateObjFromYamlFile(filePath)
            ValidationUtil.failIfObjNone(props, "No properties available in configuration file '" + filePath + "'.")
            # Add Configuration
            self.__configs[name] = AppConfig(configProps)
