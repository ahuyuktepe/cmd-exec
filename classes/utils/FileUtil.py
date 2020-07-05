import json
import os.path

class FileUtil:
    @staticmethod
    def generateObjFromJsonFile(filePath) -> dict:
        if not os.path.exists(filePath):
            raise Exception("File '" + filePath + "' is not found.")
        jsonFile = open(filePath)
        jsonStr = jsonFile.read()
        return json.loads(jsonStr)
