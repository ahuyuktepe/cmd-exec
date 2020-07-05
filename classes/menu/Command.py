
class Command:
    _id: str = None
    _description: str = None
    _executor: str = None

    def __init__(self, id: str, description: str, executor: str):
        self._id = id
        self._description = description
        self._executor = executor
