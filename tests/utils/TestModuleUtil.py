import yaml
from src.util.FileUtil import FileUtil


class TestModuleUtil:
    @staticmethod
    def generateModulesDir():
        FileUtil.makeDir(['modules'])

    @staticmethod
    def clearModulesDir():
        dirs = FileUtil.listFiles(['modules'])
        for dir in dirs:
            FileUtil.deleteDir(['modules', dir])

    @staticmethod
    def generateModuleDir(name: str):
        FileUtil.makeDir(['modules', name])
        FileUtil.makeDir(['modules', name, 'src'])
        FileUtil.makeDir(['modules', name, 'src', 'service'])

    @staticmethod
    def generateModuleFiles(name: str, settings: dict = None, config: dict = None):
        TestModuleUtil.generateModuleDir(name)
        settingsFileName = (name + '.settings.yaml')
        if settings is None:
            TestModuleUtil.saveDictionaryAsYamlFile(name, settingsFileName, {
                'name': name,
                'version': '0.0.1'
            })
        else:
            TestModuleUtil.saveDictionaryAsYamlFile(name, settingsFileName, settings)

        configFileName = (name + '.config.yaml')
        if config is not None:
            TestModuleUtil.saveDictionaryAsYamlFile(name, configFileName, config)

    @staticmethod
    def saveSettingsFile(name: str, settings: dict):
        fileName = name + '.settings.yaml'
        TestModuleUtil.saveDictionaryAsYamlFile(name, fileName, settings)

    @staticmethod
    def saveDictionaryAsYamlFile(name: str, fileName: str, values: dict):
        if values is not None:
            relativePath = ['modules', name, fileName]
            content: str = yaml.safe_dump(values)
            FileUtil.writeToFile(relativePath, content)
