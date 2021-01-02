
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
    def isNoneOrEmpty(value: str):
        return value is None or value == ''
