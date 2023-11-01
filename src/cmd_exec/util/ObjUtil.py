import importlib

class ObjUtil:
    __clsRootPath: str = None

    @staticmethod
    def setRootPath(path: str):
        if not ObjUtil.__clsRootPath:
            ObjUtil.__clsRootPath = path

    @staticmethod
    def initClassFromStr(clsPath: str, clsName: str, args: list = None, package: str = None) -> object:
        path: str = ObjUtil.__buildClassPath(clsPath)
        module = importlib.import_module(path, package)
        cls = getattr(module, clsName)
        if args is None:
            obj = cls()
        else:
            obj = cls(*args)
        return obj

    @staticmethod
    def getClassFromClsPath(clsPath: str, clsName: str, package: str = None):
        path: str = ObjUtil.__buildClassPath(clsPath)
        module = importlib.import_module(path, package)
        cls = getattr(module, clsName)
        return cls

    @staticmethod
    def __buildClassPath(clsPath: str):
        if ObjUtil.__clsRootPath is not None:
            return ObjUtil.__clsRootPath + clsPath
        return clsPath
