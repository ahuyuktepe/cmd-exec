import yaml
from src.util.FileUtil import FileUtil


class TestModuleUtil:
    @staticmethod
    def generateModulesDir():
        FileUtil.makeDir(['modules'])

    @staticmethod
    def clearModulesDir():
        pass

    @staticmethod
    def generateModuleDir(name: str):
        FileUtil.makeDir(['modules', name])

    @staticmethod
    def saveSettingsFile(name: str, settings: dict):
        fileName = name + '.settings.yaml'
        TestModuleUtil.saveDictinaryAsYamlFile(name, fileName, settings)

    @staticmethod
    def saveDictinaryAsYamlFile(name: str, fileName: str, values: dict):
        if values is not None:
            relativePath = ['modules', name, fileName]
            content: str = yaml.safe_dump(values)
            FileUtil.writeToFile(relativePath, content)
