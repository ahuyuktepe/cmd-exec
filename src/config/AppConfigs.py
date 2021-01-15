import yaml

from src.config.AppConfigConverter import AppConfigConverter
from src.config.AppConfigPath import AppConfigPath
from src.util.StrUtil import StrUtil


class AppConfigs:
    __configs: dict
    __converter: AppConfigConverter

    def __init__(self):
        self.__converter = AppConfigConverter()
        self.__configs = None

    # Setter Methods

    def addConfig(self, props: dict):
        if self.__configs is None:
            self.__configs = props
        else:
            paths: dict = self.__converter.convert(props)
            for path, value in paths.items():
                self.setConfigValue(path, value)

    def setConfigValue(self, path: str, value: object):
        if not isinstance(path, str) or StrUtil.isNoneOrEmpty(path):
            return
        configPath = AppConfigPath(path)
        self.__setNestedConfigValue(configPath, self.__configs, value)

    def __setNestedConfigValue(self, configPath: AppConfigPath, configs: dict, value: object):
        if not configPath.hasNextName():
            name = configPath.getCurrentName()
            self.__mergeValue(configs, name, value)
            return
        elif configs is None or not isinstance(configs, dict):
            raise Exception('Invalid path')
        # Drill down
        name = configPath.getCurrentName()
        configs = configs.get(name)
        configPath.nextName()
        self.__setNestedConfigValue(configPath, configs, value)

    # Getter Methods

    def getValue(self, keyPath: str = None) -> object:
        if StrUtil.isNoneOrEmpty(keyPath):
            return self.__configs
        elif not isinstance(keyPath, str):
            return None
        configPath = AppConfigPath(keyPath)
        return self.__getValueByPath(configPath)

    def print(self):
        yamlStr = yaml.dump(self.__configs)
        print(yamlStr)

    # Private Methods

    def __mergeValue(self, configs: dict, key: str, valueToMerge: object):
        if key.startswith('(+)'):
            key = key[3:]
            origValue = configs.get(key)
            # Append
            if isinstance(origValue, str):
                configs[key] = origValue + str(valueToMerge)
            elif isinstance(origValue, list):
                if isinstance(origValue, list):
                    origValue += valueToMerge
                else:
                    origValue.append(valueToMerge)
            elif origValue is None:
                configs[key] = valueToMerge
            else:
                configs[key] = origValue + valueToMerge
        elif key.startswith('(^)'):
            # Replace
            configs[key[3:]] = valueToMerge
        else:
            # Replace
            configs[key] = valueToMerge

    def __getValueByPath(self, configPath: AppConfigPath) -> object:
        if not configPath.hasNextName():
            return self.__configs.get(configPath.getCurrentName())
        name = configPath.getCurrentName()
        value = self.__configs.get(name)
        return self.__getNestedValueByPath(configPath, value)

    def __getNestedValueByPath(self, configPath: AppConfigPath, value: object) -> object:
        if not configPath.hasNextName():
            return value
        elif not isinstance(value, dict):
            return None
        configPath.nextName()
        name = configPath.getCurrentName()
        value = value.get(name)
        return self.__getNestedValueByPath(configPath, value)
