import pytest
from src.builder.AppContextBuilder import AppContextBuilder
from src.error.CmdExecError import CmdExecError
from tests.base_tester import TestBase
from tests.utils.TestFileUtil import TestFileUtil
from tests.utils.TestModuleUtil import TestModuleUtil


class TestAppContextBuilder(TestBase):

    @classmethod
    def setup_class(cls):
        TestFileUtil.setBuildDir()
        TestModuleUtil.generateModulesDir()

    def test_module_none_name_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.generateSettingsFile('test', {})
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR01'

    def test_module_none_version_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.generateSettingsFile('test', {
                'name': 'test'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR02'

    def test_module_invalid_version_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.generateSettingsFile('test', {
                'name': 'test',
                'version': 'a.b.c'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR02'

    def test_module_invalid_dependency_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestModuleUtil.generateModuleDir('test')
            TestModuleUtil.generateSettingsFile('test', {
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
            TestModuleUtil.generateSettingsFile('test', {
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
            TestModuleUtil.generateSettingsFile('test', {'name': 'test', 'version': '0.0.1'})
            TestModuleUtil.generateModuleDir('test1')
            TestModuleUtil.generateSettingsFile('test1', {
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
            TestModuleUtil.generateSettingsFile('test', {'name': 'test', 'version': '0.0.1'})
            TestModuleUtil.generateModuleDir('test1')
            TestModuleUtil.generateSettingsFile('test1', {
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
            TestModuleUtil.generateSettingsFile('test', {'name': 'test', 'version': '0.0.1'})
            TestModuleUtil.generateModuleDir('test1')
            TestModuleUtil.generateSettingsFile('test1', {
                'name': 'test1',
                'version': '0.0.1',
                'dependencies': [
                    'test|>|0.0.1'
                ]
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR09'

