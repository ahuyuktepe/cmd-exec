import pytest

from builder.AppContextBuilder import AppContextBuilder
from context.AppContext import AppContext
from error.CmdExecError import CmdExecError
from tests.src.utils.TestUtil import TestUtil


class TestAppModule:

    def setup_method(method):
        TestUtil.setupTestingEnvironment()

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def test_not_matching_name_with_files(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestUtil.buildModuleFiles('test', {
                'name': 'test1',
                'description': 'Test Module',
                'version': '0.0.1'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR20'

    def test_non_existing_version_in_module_settings(self):
        TestUtil.buildModuleFiles('test', {'name': 'test'}, {
            'name': 'Test'
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR02'

    def test_non_invalid_version_in_module_settings(self):
        TestUtil.buildModuleFiles('test', {'name': 'test'}, {
            'name': 'Test',
            'version': 'a.b.c'
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR02'

    def test_non_existing_name_in_module_settings(self):
        TestUtil.buildModuleFiles('test', {'version': '0.0.1'}, {
            'name': 'Test'
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR01'

    def test_module_properties(self):
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1'
        })
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        module = appContext.getModule('test')
        assert module.getName() == 'test'
        assert module.getDescription() == 'Test Module'
        assert module.getVersion() == '0.0.1'

    def test_module_invalid_dependency_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestUtil.buildModuleFiles('test', {
                'name': 'test',
                'version': '0.0.1',
                'dependencies': 'test_1'
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR03'

    def test_module_non_existing_dependency_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestUtil.buildModuleFiles('test', {
                'name': 'test',
                'version': '0.0.1',
                'dependencies': ['test_1']
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR07'

    def test_module_invalid_dependency_operator_validation(self):
        with pytest.raises(CmdExecError) as errInfo:
            TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'})
            TestUtil.buildModuleFiles('test1', {
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
            TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'})
            TestUtil.buildModuleFiles('test1', {
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
            TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'})
            TestUtil.buildModuleFiles('test1', {
                'name': 'test1',
                'version': '0.0.1',
                'dependencies': [
                    'test|>|0.0.1'
                ]
            })
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR09'

