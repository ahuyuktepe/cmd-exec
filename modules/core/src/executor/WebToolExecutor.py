from src.command.CmdExecutor import CmdExecutor
from src.date.Date import Date
from src.field.DateField import DateField


class WebToolExecutor(CmdExecutor):

    def run(self, fields: dict):
        field: DateField = fields.get('publish_date')
        if field is not None:
            date: Date = field.getValue()
            print('Date: ' + date.toString())
