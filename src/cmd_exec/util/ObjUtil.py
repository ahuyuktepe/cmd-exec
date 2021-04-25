import importlib
import sys, os

class ObjUtil:

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
