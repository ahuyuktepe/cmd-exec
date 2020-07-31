import importlib

class ObjUtil:

    @staticmethod
    def getClassFromStr(classPackage: str, className: str) -> object:
        module = importlib.import_module('{package}.{className}'.format(package=classPackage, className=className))
        cls = getattr(module, className)
        return cls

    @staticmethod
    def mergeDictIntoOther(srcDict: dict, destDict: dict):
        if srcDict is not None:
            for key, value in srcDict:
                destDict[key] = value
