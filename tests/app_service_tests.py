import pytest
from src.builder.AppContextBuilder import AppContextBuilder
from src.context.AppContext import AppContext
from src.error.CmdExecError import CmdExecError
from src.util.FileUtil import FileUtil
from tests.utils.TestModuleUtil import TestModuleUtil


class TestAppService:

    @classmethod
    def setup_class(cls):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModulesDir()

    @classmethod
    def teardown_class(cls):
        TestModuleUtil.clearModulesDir()

    def testing_invalid_service_props_1(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': '-'
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR24'

    def testing_invalid_service_props_2(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [{'id': None}]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR23'

    def testing_invalid_service_props_3(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [{'id': ''}]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR23'

    def testing_invalid_service_props_4(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [{'id': 'test'}]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR23'

    def testing_not_existing_service_fetch_5(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1'
        })
        with pytest.raises(CmdExecError) as errInfo:
            appContext: AppContext = AppContextBuilder.buildBaseAppContext()
            appContext.getService('testService')
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR27'

    def testing_service_init_6(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService',
                    'path': 'build.modules.test.src.service.TestService',
                    'init': True,
                    'args': ['testing']
                }
            ]
        })
        FileUtil.copyFile(['test-classes', 'service', 'TestService.py'], ['modules', 'test', 'src', 'service'])
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        service = appContext.getService('testService')
        assert service is not None
        assert service.__class__.__name__ == 'TestService'
        assert service.getId() == 'testing'

    def testing_service_init_7(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.generateModuleFiles('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testConfigService',
                    'path': 'build.modules.test.src.service.TestConfigService',
                    'init': True,
                    'args': ['appConfigs']
                }
            ]
        }, {
            'application': {
                'name': 'Test Application'
            }
        })
        FileUtil.copyFile(['test-classes', 'service', 'TestConfigService.py'], ['modules', 'test', 'src', 'service'])
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        service = appContext.getService('testConfigService')
        assert service is not None
        assert service.__class__.__name__ == 'TestConfigService'
        assert service.getName() == 'Test Application'

    def testing_service_init_8(self):
        # Given
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.generateModuleFiles('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService',
                    'path': 'build.modules.test.src.service.TestService',
                    'args': ['Test Service']
                }, {
                    'id': 'testService1',
                    'path': 'build.modules.test.src.service.TestService1',
                    'args': ['Test Service 1', '@testService']
                }, {
                    'id': 'testService2',
                    'path': 'build.modules.test.src.service.TestService2',
                    'init': True,
                    'args': ['Test Service 2', '@testService', '@testService1']
                }
            ]
        })
        FileUtil.copyFile(['test-classes', 'service', 'TestService.py'], ['modules', 'test', 'src', 'service'])
        FileUtil.copyFile(['test-classes', 'service', 'TestService1.py'], ['modules', 'test', 'src', 'service'])
        FileUtil.copyFile(['test-classes', 'service', 'TestService2.py'], ['modules', 'test', 'src', 'service'])

        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        service = appContext.getService('testService')
        service1 = appContext.getService('testService1')
        service2 = appContext.getService('testService2')

        # Then
        assert service is not None
        assert service1 is not None
        assert service2 is not None
        assert service.__class__.__name__ == 'TestService'
        assert service1.__class__.__name__ == 'TestService1'
        assert service2.__class__.__name__ == 'TestService2'
        assert service.getId() == 'Test Service'
        assert service1.getId() == 'Test Service 1'
        assert service2.getId() == 'Test Service 2'

        srvc = service1.getService()
        assert srvc is not None
        assert srvc.__class__.__name__ == 'TestService'

        srvc = service2.getService()
        assert srvc is not None
        assert srvc.__class__.__name__ == 'TestService'

        srvc = service2.getService1()
        assert srvc is not None
        assert srvc.__class__.__name__ == 'TestService1'

    def testing_service_on_demand_init_9(self):
        # Given
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.generateModuleFiles('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService',
                    'path': 'build.modules.test.src.service.TestService',
                    'args': ['Test Service']
                }, {
                    'id': 'testService1',
                    'path': 'build.modules.test.src.service.TestService1',
                    'args': ['Test Service 1', '@testService']
                }, {
                    'id': 'testService2',
                    'path': 'build.modules.test.src.service.TestService2',
                    'args': ['Test Service 2', '@testService', '@testService1']
                }
            ]
        })
        FileUtil.copyFile(['test-classes', 'service', 'TestService.py'], ['modules', 'test', 'src', 'service'])
        FileUtil.copyFile(['test-classes', 'service', 'TestService1.py'], ['modules', 'test', 'src', 'service'])
        FileUtil.copyFile(['test-classes', 'service', 'TestService2.py'], ['modules', 'test', 'src', 'service'])

        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        service = appContext.getService('testService')
        service1 = appContext.getService('testService1')
        service2 = appContext.getService('testService2')

        # Then
        assert service is not None
        assert service1 is not None
        assert service2 is not None
        assert service.__class__.__name__ == 'TestService'
        assert service1.__class__.__name__ == 'TestService1'
        assert service2.__class__.__name__ == 'TestService2'
        assert service.getId() == 'Test Service'
        assert service1.getId() == 'Test Service 1'
        assert service2.getId() == 'Test Service 2'

        srvc = service1.getService()
        assert srvc is not None
        assert srvc.__class__.__name__ == 'TestService'

        srvc = service2.getService()
        assert srvc is not None
        assert srvc.__class__.__name__ == 'TestService'

        srvc = service2.getService1()
        assert srvc is not None
        assert srvc.__class__.__name__ == 'TestService1'

    def testing_service_init_10(self):
        # Given
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.generateModuleFiles('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService',
                    'path': 'build.modules.test.src.service.TestService',
                    'args': ['Test Service']
                }
            ]
        })
        TestModuleUtil.generateModuleFiles('test1', {
            'name': 'test1',
            'description': 'Test Module 1',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService1',
                    'path': 'build.modules.test1.src.service.TestService1',
                    'args': ['Test Service 1', '@test.testService']
                }
            ]
        })
        FileUtil.copyFile(['test-classes', 'service', 'TestService.py'], ['modules', 'test', 'src', 'service'])
        FileUtil.copyFile(['test-classes', 'service', 'TestService1.py'], ['modules', 'test1', 'src', 'service'])
        # When
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        service = appContext.getService('testService')
        service1 = appContext.getService('testService1')
        # Then
        assert service is not None
        assert service1 is not None
        assert service.__class__.__name__ == 'TestService'
        assert service1.__class__.__name__ == 'TestService1'
        assert service.getId() == 'Test Service'
        assert service1.getId() == 'Test Service 1'
        srvc = service1.getService()
        assert srvc is not None
        assert srvc.__class__.__name__ == 'TestService'

    def testing_invalid_service_props_11(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService1',
                    'path': 'build.modules.test1.src.service.TestService1',
                    'init': 'test'
                }
            ]
        })
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR29'

    def testing_invalid_service_props_12(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModuleDir('test')
        TestModuleUtil.saveSettingsFile('test', {
            'name': 'test',
            'description': 'Test Module',
            'version': '0.0.1',
            'services': [
                {
                    'id': 'testService',
                    'path': 'build.modules.test.src.service.TestService3',
                    'init': True
                }
            ]
        })
        FileUtil.copyFile(['test-classes', 'service', 'TestService3.py'], ['modules', 'test', 'src', 'service'])
        with pytest.raises(CmdExecError) as errInfo:
            AppContextBuilder.buildBaseAppContext()
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR28'

