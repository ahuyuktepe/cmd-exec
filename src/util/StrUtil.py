

class StrUtil:
    @staticmethod
    def getFilePropertiesFromStr(sid: str) -> dict:
        arr: list = sid.split('.')
        props: dict = {'module': 'core', 'file': None}
        if len(arr) > 1:
            props['module'] = arr[0]
            props['file'] = arr[1]
        elif len(arr) == 1:
            props['file'] = arr[0]
        return props

    @staticmethod
    def getClassMethodMapFromStr(clsPath: str, defaultMethod: str = None) -> dict:
        arr: list = clsPath.split('.')
        idCount = len(arr)
        if idCount == 3:
            return {
                'module': arr[0],
                'class': arr[1],
                'method': arr[2]
            }
        elif idCount == 2:
            return {
                'module': arr[0],
                'class': arr[1],
                'method': defaultMethod
            }
        else:
            raise Exception('Given class path is invalid.')

    @staticmethod
    def isNoneOrEmpty(value: str):
        return value is None or value == ''

    @staticmethod
    def isVersionSyntaxInvalid(version: str) -> bool:
        if version is None:
            return True
        values = version.split('.')
        for value in values:
            if not value.isnumeric():
                return True
        return False

    @staticmethod
    def prefillVersion(version: str, fillCount: int = 2) -> str:
        arr = []
        if version is not None:
            values = version.split('.')
            for value in values:
                arr.append(value.zfill(fillCount))
        return '.'.join(arr)
