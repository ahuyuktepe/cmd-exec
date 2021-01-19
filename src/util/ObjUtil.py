import importlib


class ObjUtil:

    @staticmethod
    def initClassFromStr(classPath: str, className: str, args: list = None) -> object:
        module = importlib.import_module(classPath)
        cls = getattr(module, className)
        if args is None:
            obj = cls()
        else:
            obj = cls(*args)
        return obj
