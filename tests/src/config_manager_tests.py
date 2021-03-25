import pytest
from config.ConfigManager import ConfigManager
from error.CmdExecError import CmdExecError


class TestConfigManager:
    __configManager: ConfigManager

    def setup_method(self, method):
        self.__configManager = ConfigManager({
            'user': {
                'first_name': 'Test',
                'last_name': 'User',
                'bank': {
                    'name': 'TD Bank',
                    'balance': 100,
                    'address': {
                        'city': 'Hillsborough',
                        'state': 'NJ',
                        'zip': '08844'
                    }
                }
            },
            'siblings': {
                'names': [
                    {'first_name': 'Sibling 1', 'last_name': 'User 1'}
                ],
                'ages': [19, 32, 15, 9]
            }
        })

    def test_fetch_map(self):
        bank = self.__configManager.getValue(['user', 'bank'])
        assert bank is not None and bank['name'] == 'TD Bank' and bank['balance'] == 100

    def test_fetch_str(self):
        city = self.__configManager.getValue(['user', 'bank', 'address', 'city'])
        assert city == 'Hillsborough'

    def test_fetch_list(self):
        city = self.__configManager.getValue(['siblings', 'ages'])
        assert city == [19, 32, 15, 9]

    def test_str_to_int_mismatch(self):
        newConfigs: dict = {
            'user': {
                'first_name': 100
            }
        }
        with pytest.raises(CmdExecError) as err:
            self.__configManager.save(newConfigs)
        error: CmdExecError = err.value
        assert error.getCode() == 'ERR64'

    def test_list_to_str_mismatch(self):
        newConfigs: dict = {
            'siblings': {
                'ages': 'test'
            }
        }
        with pytest.raises(CmdExecError) as err:
            self.__configManager.save(newConfigs)
        error: CmdExecError = err.value
        assert error.getCode() == 'ERR64'

    def test_replace_list(self):
        newConfigs: dict = {
            'siblings': {
                'ages': [1]
            }
        }
        self.__configManager.save(newConfigs)
        ages = self.__configManager.getValue(['siblings', 'ages'])
        assert ages == [1]

    def test_replace_str(self):
        newConfigs: dict = {
            'user': {
                'first_name': 'Test 1'
            }
        }
        self.__configManager.save(newConfigs)
        firstName = self.__configManager.getValue(['user', 'first_name'])
        assert firstName == 'Test 1'

    def test_replace_int(self):
        newConfigs: dict = {
            'user': {
                'bank': {
                    'balance': 50
                }
            }
        }
        self.__configManager.save(newConfigs)
        balance = self.__configManager.getValue(['user', 'bank', 'balance'])
        assert balance == 50

    def test_append_list(self):
        newConfigs: dict = {
            'siblings': {
                '(+)ages': [1]
            }
        }
        self.__configManager.save(newConfigs)
        ages = self.__configManager.getValue(['siblings', 'ages'])
        assert ages == [19, 32, 15, 9, 1]

    def test_append_str(self):
        newConfigs: dict = {
            'user': {
                '(+)first_name': ' User 1'
            }
        }
        self.__configManager.save(newConfigs)
        firstName = self.__configManager.getValue(['user', 'first_name'])
        assert firstName == 'Test User 1'

    def test_append_int(self):
        newConfigs: dict = {
            'user': {
                'bank': {
                    '(+)balance': 50
                }
            }
        }
        self.__configManager.save(newConfigs)
        balance = self.__configManager.getValue(['user', 'bank', 'balance'])
        assert balance == 150
