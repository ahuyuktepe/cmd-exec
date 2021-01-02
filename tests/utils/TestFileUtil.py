import yaml


class TestFileUtil:

    @staticmethod
    def saveObjIntoFileAsYaml(path: str, data: object):
        content: str = yaml.safe_dump(data)
        TestFileUtil.writeFile(path, content)

    @staticmethod
    def writeFile(path: str, content: str):
        file = open(path, 'w')
        file.write(content)
        file.close()
