from cmd_exec.database.DomainObject import DomainObject


class User(DomainObject):
    _properties = {
        'table': 'users',
        'columns': [
            {'name': 'first_name', 'type': 'text', 'is_primary_key': True},
            {'name': 'last_name', 'type': 'text'}
        ]
    }

    def __init__(self):
        super().__init__(self._properties)
