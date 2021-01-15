import os

import yaml

from src.util.FileUtil import FileUtil


class TestFileUtil:

    @staticmethod
    def setBuildDir():
        buildDirPath = os.environ['APP_RUNNER_ROOT_PATH'] + os.sep + 'build'
        FileUtil.makeDir(buildDirPath)
        os.environ['APP_RUNNER_ROOT_PATH'] = buildDirPath

    @staticmethod
    def saveObjIntoFileAsYaml(path: str, data: object):
        content: str = yaml.safe_dump(data)
        TestFileUtil.writeFile(path, content)

    @staticmethod
    def writeFile(path: str, content: str):
        file = open(path, 'w')
        file.write(content)
        file.close()
