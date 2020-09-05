
class Form:
    title: str
    fields: list

    def __init__(self, title: str, fields: list):
        self.title = title
        self.fields = fields