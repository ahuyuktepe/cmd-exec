from app_runner.extension.ContextAware import ContextAware
from app_runner.field.Field import Field


class CustomValueGetter(ContextAware):

    def getOptions(self, field: Field) -> list:
        return [
            {"id": "ankara", "label": "Ankara"},
            {"id": "kirikkale", "label": "Kirikkale"}
        ]

    def getMultiSelectFieldOptions(self, field: Field):
        self._appContext.getService('logService').info('getMultiSelectFieldOptions')
        print('getMultiSelectFieldOptions')
        return [
            {"id": "08540", "label": "Princeton, NJ"}
        ]
