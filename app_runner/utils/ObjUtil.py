import importlib

class ObjUtil:

    @staticmethod
    def getClassFromStr(classPath: str, className: str) -> object:
        module = importlib.import_module(classPath)
        cls = getattr(module, className)
        return cls

    @staticmethod
    def mergeDictIntoOther(srcDict: dict, destDict: dict):
        if srcDict is not None:
            for key, value in srcDict:
                destDict[key] = value

    @staticmethod
    def isStr(val: object) -> bool:
        return isinstance(val, str)

    @staticmethod
    def isList(val: object) -> bool:
        return isinstance(val, list)

    @staticmethod
    def hasMethod(obj: object, methodName: str) -> bool:
        return hasattr(obj, methodName)
