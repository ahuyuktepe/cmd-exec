import pytest
from src.builder.AppContextBuilder import AppContextBuilder
from src.context.AppContext import AppContext
from src.error.CmdExecError import CmdExecError
from tests.utils.TestModuleUtil import TestModuleUtil


class TestAppModule:

    @classmethod
    def setup_class(cls):
        TestModuleUtil.generateModulesDir()

    @classmethod
    def teardown_class(cls):
        TestModuleUtil.clearModulesDir()

    def test_not_matching_name_with_files(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {
                'name': 'test1',
                'description': 'Test Module',
                'version': '0.0.1'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR20'

    def test_module_properties(self):
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1'
        })
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        module = appContext.getModule('test')
        assert module.getName() == 'test'
        assert module.getDescription() == 'Test Module'
        assert module.getVersion() == '0.0.1'

    def test_module_none_name_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {})
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR01'

    def test_module_none_version_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {
                'name': 'test'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR02'

    def test_module_invalid_version_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {
                'name': 'test',
                'version': 'a.b.c'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR02'

    def test_module_invalid_dependency_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {
                'name': 'test',
                'version': '0.0.1',
                'dependencies': 'test'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR03'

    def test_module_none_dependency_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {
                'name': 'test',
                'version': '0.0.1',
                'dependencies': [
                    'core'
                ]
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR07'

    def test_module_invalid_dependency_operator_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {'name': 'test', 'version': '0.0.1'})
            TestModuleUtil.generateModuleDir('test1')
            TestModuleUtil.saveSettingsFile('test1', {
                'name': 'test1',
                'version': '0.0.1',
                'dependencies': [
                    'test|x|0.0.1'
                ]
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR16'

    def test_module_invalid_dependency_version_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {'name': 'test', 'version': '0.0.1'})
            TestModuleUtil.generateModuleDir('test1')
            TestModuleUtil.saveSettingsFile('test1', {
                'name': 'test1',
                'version': '0.0.1',
                'dependencies': [
                    'test|=|0.0.1a'
                ]
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR17'

    def test_module_dependency_version_not_matching_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.saveSettingsFile('test', {'name': 'test', 'version': '0.0.1'})
            TestModuleUtil.generateModuleDir('test1')
            TestModuleUtil.saveSettingsFile('test1', {
                'name': 'test1',
                'version': '0.0.1',
                'dependencies': [
                    'test|>|0.0.1'
                ]
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR09'

