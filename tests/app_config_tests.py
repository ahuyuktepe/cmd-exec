import pytest
from src.builder.AppContextBuilder import AppContextBuilder
from src.error.CmdExecError import CmdExecError
from tests.utils.TestModuleUtil import TestModuleUtil


class TestAppConfig:

    @classmethod
    def setup_class(cls):
        TestModuleUtil.generateModulesDir()

    @classmethod
    def teardown_class(cls):
        TestModuleUtil.clearModulesDir()

    def test_unsupport_character_in_config(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveDictionaryAsYamlFile('test', 'test.settings.yaml', {
                'name': 'test',
                'version': '0.0.1'
            })
            TestModuleUtil.saveDictionaryAsYamlFile('test', 'test.config.yaml', {'name.': 'test'})
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR18'

    def test_config(self):
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveDictionaryAsYamlFile('test', 'test.settings.yaml', {
            'name': 'test',
            'version': '0.0.1'
        })
        TestModuleUtil.saveDictionaryAsYamlFile('test', 'test.config.yaml', {'name': 'test'})
        appContext = AppContextBuilder.buildBaseAppContext()
        name = appContext.getConfig('name')
        assert name == 'test'

    def test_merge_config(self):
        TestModuleUtil.generateModuleFiles('test', None, {
            'a': {'b': 1}
        })
        TestModuleUtil.generateModuleFiles('test1', None, {
            'a': {'b': 2}
        })
        appContext = AppContextBuilder.buildBaseAppContext()
        value = appContext.getConfig('a.b')
        assert value == 2

    def test_wilcard_in_config(self):
        TestModuleUtil.generateModuleFiles('test', None, {
            'a': {'b': 1}
        })
        TestModuleUtil.generateModuleFiles('test1', None, {
            'a': {'(+)b': 2}
        })
        appContext = AppContextBuilder.buildBaseAppContext()
        value = appContext.getConfig('a.b')
        assert value == 3

    def test_wilcard_in_config_1(self):
        TestModuleUtil.generateModuleFiles('test', None, {
            'a': {'b': [1]}
        })
        TestModuleUtil.generateModuleFiles('test1', None, {
            'a': {'(+)b': [2]}
        })
        appContext = AppContextBuilder.buildBaseAppContext()
        value = appContext.getConfig('a.b')
        assert value == [1, 2]

    def test_wilcard_in_config_2(self):
        TestModuleUtil.generateModuleFiles('test', None, {
            'a': {'b': 'test'}
        })
        TestModuleUtil.generateModuleFiles('test1', None, {
            'a': {'(+)b': '1'}
        })
        appContext = AppContextBuilder.buildBaseAppContext()
        value = appContext.getConfig('a.b')
        assert value == 'test1'