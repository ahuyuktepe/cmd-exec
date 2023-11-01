import pytest

from cmd_exec.builder.AppContextBuilder import AppContextBuilder
from cmd_exec.context.AppContext import AppContext
from cmd_exec.error.CmdExecError import CmdExecError
from cmd_exec.module.AppModule import AppModule
from tests.src.utils.TestUtil import TestUtil


class TestAppConfig:

    def setup_method(method):
        TestUtil.setupTestingEnvironment()

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def test_config(self):
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {'name': 'test'})
        appContext = AppContextBuilder.buildBaseAppContext()
        name = appContext.getConfig('name')
        assert name == 'test'

    def test_append_str(self):
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {
            'a': {'b': 'test'}
        })
        TestUtil.buildModuleFiles('test1', {'name': 'test1', 'version': '0.0.1'}, {
            'a': {'(+)b': '1'}
        })
        appContext = AppContextBuilder.buildBaseAppContext()
        value = appContext.getConfig('a.b')
        assert value == 'test1'

    def test_append_int(self):
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {
            'a': {'c': 100}
        })
        TestUtil.buildModuleFiles('test1', {'name': 'test1', 'version': '0.0.1'}, {
            'a': {'(+)c': 50}
        })
        appContext = AppContextBuilder.buildBaseAppContext()
        value = appContext.getConfig('a.c')
        assert value == 150

    def test_append_list(self):
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {
            'a': {'d': [1, 2, 3]}
        })
        TestUtil.buildModuleFiles('test1', {'name': 'test1', 'version': '0.0.1'}, {
            'a': {'(+)d': [4]}
        })
        appContext = AppContextBuilder.buildBaseAppContext()
        value = appContext.getConfig('a.d')
        assert value == [1, 2, 3, 4]

    def test_unsupported_character_in_config(self):
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {
            'name.': 'Test'
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR18'

    def test_module_with_empty_config_file(self):
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {})
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        module: AppModule = appContext.getModule('test')
        assert module.getName() == 'test' and module.getVersion() == '0.0.1'
