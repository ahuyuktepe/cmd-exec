import os

from app_runner.utils.FileUtil import FileUtil


class TestFileUtil:

    @staticmethod
    def setRootPath():
        os.environ['APP_RUNNER_ROOT_PATH'] = os.environ['APP_RUNNER_ROOT_PATH'] + os.sep + 'temp'

    @staticmethod
    def createMainConfig(configData: object):
        FileUtil.makeDirsInSrcDir(os.environ['APP_RUNNER_ROOT_PATH'], ['resources', 'conf'])
        mainConfFilePath = FileUtil.getAbsolutePath(['resources', 'conf', 'main.yaml'])
        FileUtil.saveObjIntoFileAsYaml(mainConfFilePath, configData)

    @staticmethod
    def createModuleConfig(module: str, menu: str, configData: object):
        FileUtil.makeDirsInSrcDir(os.environ['APP_RUNNER_ROOT_PATH'], ['modules', module, 'menus'])
        mainConfFilePath = FileUtil.getAbsolutePath(['modules', module, 'menus', menu]) + '.yaml'
        FileUtil.saveObjIntoFileAsYaml(mainConfFilePath, configData)
