import importlib
import sys, os

class ObjUtil:

    @staticmethod
    def initialize(env: str):
        if env == 'production':
            path = os.environ['APP_RUNNER_ROOT_PATH']
            sys.path.append(path)
        elif env == 'test':
            path = os.environ['APP_RUNNER_ROOT_PATH'] + os.sep + 'tests' + os.sep + 'target'
            sys.path.append(path)

    @staticmethod
    def initClassFromStr(clsPath: str, clsName: str, args: list = None) -> object:
        module = importlib.import_module(clsPath)
        cls = getattr(module, clsName)
        if args is None:
            obj = cls()
        else:
            obj = cls(*args)
        return obj

    @staticmethod
    def getClassFromClsPath(clsPath: str, clsName: str):
        module = importlib.import_module(clsPath)
        cls = getattr(module, clsName)
        return cls
