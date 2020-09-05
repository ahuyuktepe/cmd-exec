import importlib

class ObjUtil:

    @staticmethod
    def getClassFromStr(classPackage: str, className: str) -> object:
        classPath: str = '{package}.{className}'.format(
            package=classPackage,
            className=className
        )
        module = importlib.import_module(classPath)
        cls = getattr(module, className)
        return cls

    @staticmethod
    def mergeDictIntoOther(srcDict: dict, destDict: dict):
        if srcDict is not None:
            for key, value in srcDict:
                destDict[key] = value
