import os
import pytest
from tests.src.utils.TestUtil import TestUtil

class MyPlugin:
    def pytest_runtest_setup(item):
        TestUtil.setupTestingEnvironment()

    def pytest_runtest_teardown(item, nextitem):
        TestUtil.destroyTestingEnvironment()

plugin = MyPlugin()
testsDir = os.path.sep.join(['C:', 'Projects', 'cmd-exec', 'tests', 'src'])
targetTests = ['database_service_tests.py']
testFiles = os.listdir(testsDir)
for fileName in testFiles:
    if fileName.endswith("tests.py") and fileName in targetTests:
        filePath = os.path.sep.join([testsDir, fileName])
        print("\n\n===============================================================================")
        print("****************** Running Tests In '" + fileName + "' *********************")
        pytest.main([filePath], plugins=[plugin])
