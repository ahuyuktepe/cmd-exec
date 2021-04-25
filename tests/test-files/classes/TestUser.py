from cmd_exec.database.DomainObject import DomainObject


class TestUser(DomainObject):

    def __init__(self):
        super().__init__()

    def setProperties(self):
        self._properties = {
            'table': 'users',
            'columns': [
                {'name': 'first_name', 'type': 'text', 'is_primary_key': True},
                {'name': 'last_name', 'type': 'text'}
            ]
        }
