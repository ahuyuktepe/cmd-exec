from cmd_exec.classes.Option import Option
from cmd_exec.field.OptionProvider import OptionProvider


class NameOptionProvider(OptionProvider):

    def getOptions(self) -> list:
        return [
            Option('test_from_provider', 'Test From Provider'),
            Option('test_from_provider_1', 'Test From Provider 1')
        ]
