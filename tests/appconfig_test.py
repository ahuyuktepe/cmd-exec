from app_runner.app.config.AppConfig import AppConfig
from app_runner.errors.InvalidConfigPathError import InvalidConfigPathError
import os
import pytest

class TestAppConfig:
    path = '../resources/args/test.config.json'
    jsonStr = '''
        {
            "a": "value_a",
            "b": {
                "c": "value_c"
            },
            "d": [
                { "e": 1, "f": "value_f", "l": { "m": 1 } }
            ],
            "f": {
                "g": { 
                    "h": "value_h",
                    "i": "value_i",
                    "k": 2 ,
                    "o": ["value_o"]
                }
            },
            "j": 1
        }
    '''
    appConfig: AppConfig

    def setup(self):
        file = open(self.path, 'w')
        # Test invalid json format
        file.write(self.jsonStr)
        file.close()
        self.appConfig = AppConfig(self.path)

    def cleanUp(self):
        os.remove(self.path)

    def test_getObjValue(self):
        self.setup()
        assert self.appConfig.getObjValue(None) is None
        assert self.appConfig.getObjValue('') is None
        assert self.appConfig.getObjValue('test') is None
        assert self.appConfig.getObjValue('a') == 'value_a'
        assert self.appConfig.getObjValue('b.c') == 'value_c'
        assert self.appConfig.getObjValue('f.g.i') == 'value_i'
        assert self.appConfig.getObjValue('f.g.k') == 2
        values = self.appConfig.getObjValue('f.g.o')
        assert isinstance(values, list) and values[0] == 'value_o'
        with pytest.raises(InvalidConfigPathError):
            self.appConfig.getObjValue('d.e')
        self.cleanUp()
