import importlib


class ObjUtil:
    __clsPathPrefix: str = None
    __environment: str = 'production'

    @staticmethod
    def setEnvironment(env: str):
        if env is not None and isinstance(env, str):
            ObjUtil.__environment = env

    @staticmethod
    def initialize():
        if ObjUtil.__clsPathPrefix is None:
            if ObjUtil.__environment == 'test':
                ObjUtil.__clsPathPrefix = 'tests.target.'
            else:
                ObjUtil.__clsPathPrefix = ''

    @staticmethod
    def initClassFromStr(clsPath: str, clsName: str, args: list = None) -> object:
        path = ObjUtil.__clsPathPrefix + clsPath
        module = importlib.import_module(path)
        cls = getattr(module, clsName)
        if args is None:
            obj = cls()
        else:
            obj = cls(*args)
        return obj

    @staticmethod
    def getClassFromClsPath(clsPath: str, clsName: str):
        path = ObjUtil.__clsPathPrefix + clsPath
        module = importlib.import_module(path)
        cls = getattr(module, clsName)
        return cls
