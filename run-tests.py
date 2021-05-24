import os
import pytest
from _pytest.config import ExitCode

class MyPlugin:
    failedTestCount: int

    def __init__(self):
        self.failedTestCount = 0

    def pytest_sessionfinish(self, session):
        if session.exitstatus == ExitCode.TESTS_FAILED:
            self.failedTestCount += 1

    def isAnyTestFailed(self) -> bool:
        return self.failedTestCount > 0

# Fetch Tests
plugin = MyPlugin()
pathArr = ["C:", "Users", "humalp", "Projects", "command-executor"]
path = os.path.sep.join(pathArr)
os.environ["APP_RUNNER_ROOT_PATH"] = path

# Run Tests
testsDir = os.path.sep.join([path, "tests", "src"])
fileNames = os.listdir(testsDir)
for fileName in fileNames:
    if fileName.endswith("tests.py"):
        filePath = os.path.sep.join([testsDir, fileName])
        print("\n\n===============================================================================")
        print("****************** Running Tests In '" + fileName + "' *********************")
        pytest.main([filePath], plugins=[plugin])

# Print Results
print("\nFailed Tests: " + str(plugin.failedTestCount))