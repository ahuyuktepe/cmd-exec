import pytest

from src.builder.AppContextBuilder import AppContextBuilder
from src.context.AppContext import AppContext
from src.error.CmdExecError import CmdExecError
from src.util.ObjUtil import ObjUtil
from tests.src.utils.TestUtil import TestUtil


class TestAppService:

    def setup_method(method):
        TestUtil.setupTestingEnvironment()
        ObjUtil.initialize()

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def test_invalid_service_props(self):
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': '-'
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR24'

    def test_invalid_service_props_1(self):
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [{'id': None}]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR23'

    def test_invalid_service_props_2(self):
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [{'id': ''}]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR23'

    def test_invalid_service_props_3(self):
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [{'id': 'test'}]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR23'

    def test_invalid_service_props_4(self):
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [{'id': 'test'}]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR23'

    def test_service_init(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService', 'class': 'TestService'}
            ]
        })
        TestUtil.useServicesInModule(['TestService'], 'test')
        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        # Then
        service = appContext.getService('testService')
        assert service is not None and service.getName() == 'TestService'

    def test_service_init_1(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService', 'path': 'modules.test.src.service.TestService'}
            ]
        })
        TestUtil.useServicesInModule(['TestService'], 'test')
        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        # Then
        service = appContext.getService('testService')
        assert service is not None and service.getName() == 'TestService'

    def test_service_init_2(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService',
                    'init': True,
                    'path': 'modules.test.src.service.TestService'
                }
            ]
        })
        TestUtil.useServicesInModule(['TestService'], 'test')
        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        # Then
        service = appContext.getService('testService')
        assert service is not None and service.getName() == 'TestService'

    def test_service_init_3(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService1', 'class': 'TestService1'}
            ]
        })
        TestUtil.useServicesInModule(['TestService1'], 'test')
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])
        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        # Then
        service = appContext.getService('testService1')
        assert service is not None and service.getAppName() == 'Main Application'

    def test_appconfigs_injection_into_service(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService4', 'class': 'TestService4', 'args': ['appConfigs']}
            ]
        })
        TestUtil.useServicesInModule(['TestService4'], 'test')
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])
        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        # Then
        service = appContext.getService('testService4')
        assert service is not None and service.getAppName() == 'Main Application'

    def test_service_not_extending_from_app_service(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService5', 'class': 'TestService5'}
            ]
        })
        TestUtil.useServicesInModule(['TestService5'], 'test')
        with pytest.raises(CmdExecError) as err:
            appContext: AppContext = AppContextBuilder.buildBaseAppContext()
            appContext.getService('testService5')
        error: CmdExecError = err.value
        assert error.getCode() == 'ERR28'

    def test_service_not_extending_from_app_service_with_init_true(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService5', 'class': 'TestService5', 'init': True}
            ]
        })
        TestUtil.useServicesInModule(['TestService5'], 'test')
        with pytest.raises(CmdExecError) as err:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = err.value
        assert error.getCode() == 'ERR28'

    def test_service_injecting_nested_services(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService', 'class': 'TestService'},
                {'id': 'testService3', 'class': 'TestService3', 'args': ['@testService']},
                {'id': 'testService6', 'class': 'TestService6', 'args': ['Testing', '@testService', '@testService3']}
            ]
        })
        TestUtil.useServicesInModule(['TestService', 'TestService3', 'TestService6'], 'test')
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        testService6 = appContext.getService('testService6')
        description = testService6.getDescription()
        assert description == 'name: Testing | testService: TestService | testService3: TestService'

    def test_invalid_init_value(self):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1',
            'services': [
                {'id': 'testService', 'class': 'TestService', 'init': 'test'}
            ]
        })
        TestUtil.useServicesInModule(['TestService'], 'test')
        with pytest.raises(CmdExecError) as err:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = err.value
        assert error.getCode() == 'ERR29'
