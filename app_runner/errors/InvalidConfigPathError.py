
class InvalidConfigPathError(Exception):

    def __init__(self, msg: str = None):
        if msg is None:
            super().__init__("Config path contains none dictionary object.")
        else:
            super().__init__(msg)
