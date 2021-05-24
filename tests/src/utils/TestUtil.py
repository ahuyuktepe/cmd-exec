from cmd_exec.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestFileUtil import TestFileUtil


class TestUtil:

    @staticmethod
    def setupTestingEnvironment():
        CmdExecAppRunner.initialize('test')
        TestUtil.__clearTargetDirectory()
        TestUtil.__buildModulesDirectory()
        TestUtil.__copyModules()
        TestUtil.__buildResourcesDirectory()
        TestFileUtil.copyDirectory(['src'], ['tests', 'target', 'src'])

    @staticmethod
    def destroyTestingEnvironment():
        TestUtil.__clearTargetDirectory()

    @staticmethod
    def __clearTargetDirectory():
        path = ['tests', 'target']
        if TestFileUtil.doesDirectoryExist(path):
            dirs = TestFileUtil.listFiles(path)
            for dirName in dirs:
                TestFileUtil.deleteDir(['tests', 'target', dirName])

    @staticmethod
    def __copyModules():
        if TestFileUtil.doesDirectoryExist(['modules']):
            dirs = TestFileUtil.listFiles(['modules'])
            for srcDir in dirs:
                srcPath = ['modules', srcDir]
                TestFileUtil.makeDir(srcPath)
                TestFileUtil.copyDirectory(srcPath, ['tests', 'target', 'modules', srcDir])

    @staticmethod
    def __buildModulesDirectory():
        path = ['tests', 'target', 'modules']
        TestFileUtil.makeDir(path)

    @staticmethod
    def __buildResourcesDirectory():
        path = ['tests', 'target', 'resources']
        TestFileUtil.deleteDir(path)
        TestFileUtil.makeDir(path)
        path = ['tests', 'target', 'resources', 'arguments']
        TestFileUtil.makeDir(path)
        path = ['tests', 'target', 'resources', 'commands']
        TestFileUtil.makeDir(path)
        path = ['tests', 'target', 'resources', 'configs']
        TestFileUtil.makeDir(path)
        path = ['tests', 'target', 'resources', 'databases']
        TestFileUtil.makeDir(path)

    @staticmethod
    def useCmdFilesInModule(cmdFileNames: list, moduleName: str):
        for fileName in cmdFileNames:
            srcFilePath = ['tests', 'test-files', 'commands', fileName + '.yaml']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'commands', fileName + '.yaml']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useCmdFilesInCommandsDir(cmdFileNames: list):
        for fileName in cmdFileNames:
            srcFilePath = ['tests', 'test-files', 'commands', fileName + '.yaml']
            dstDirPath = ['tests', 'target', 'resources', 'commands', fileName + '.yaml']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useArgFilesInArgumentsDir(argFileNames: list):
        for fileName in argFileNames:
            srcFilePath = ['tests', 'test-files', 'arguments', fileName]
            dstDirPath = ['tests', 'target', 'resources', 'arguments', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useConfigFilesInConfigsDir(argFileNames: list):
        for fileName in argFileNames:
            srcFilePath = ['tests', 'test-files', 'configs', fileName]
            dstDirPath = ['tests', 'target', 'resources', 'configs', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useDatabaseFilesInConfigsDir(argFileNames: list):
        for fileName in argFileNames:
            srcFilePath = ['tests', 'test-files', 'databases', fileName]
            dstDirPath = ['tests', 'target', 'resources', 'databases', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useServicesInModule(srvClsNames: list, moduleName: str):
        for fileName in srvClsNames:
            srcFilePath = ['tests', 'test-files', 'services', fileName + '.py']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'service', fileName + '.py']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useExecutorsInModule(execClsNames: list, moduleName: str):
        for fileName in execClsNames:
            srcFilePath = ['tests', 'test-files', 'executors', fileName + '.py']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'executor', fileName + '.py']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useExecutorInModuleAsInGivenName(srcClsName: str, destClsName: str, moduleName: str):
        srcFilePath = ['tests', 'test-files', 'executors', srcClsName + '.py']
        dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'executor', destClsName + '.py']
        TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useFieldsInModule(fieldClsNames: list, moduleName: str):
        for fileName in fieldClsNames:
            srcFilePath = ['tests', 'test-files', 'fields', fileName]
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'field', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useClassFileInModule(fieldClsNames: list, moduleName: str):
        for fileName in fieldClsNames:
            srcFilePath = ['tests', 'test-files', 'classes', fileName]
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'classes', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useProvidersInModule(providers: list, moduleName: str):
        for fileName in providers:
            srcFilePath = ['tests', 'test-files', 'providers', fileName + '.py']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'provider', fileName + '.py']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useAppRunnerInModule(runners: list, moduleName: str):
        for fileName in runners:
            srcFilePath = ['tests', 'test-files', 'app', fileName + '.py']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'app', fileName + '.py']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def buildModuleFiles(name: str, settings: dict = {}, config: dict = {}):
        # Generating Module Directories
        path = ['tests', 'target', 'modules', name]
        TestFileUtil.makeDir(path)
        TestFileUtil.makeDirs(path, ['commands'])
        srcPath = path + ['src']
        TestFileUtil.makeDir(srcPath)
        TestFileUtil.makeDirs(srcPath, ['app', 'executor', 'field', 'service', 'provider', 'classes'])
        # Saving Settings File
        settingsFilePath = ['tests', 'target', 'modules', name, (name + '.settings.yaml')]
        TestFileUtil.saveDictAsYamlFile(settings, settingsFilePath)
        # Saving Config File
        configFilePath = ['tests', 'target', 'modules', name, (name + '.config.yaml')]
        TestFileUtil.saveDictAsYamlFile(config, configFilePath)
