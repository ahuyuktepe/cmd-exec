
class InvalidJsonStrError(Exception):

    def __init__(self):
        super().__init__('Json string is not valid.')
