from app_runner.app.AppRunner import AppRunner
from app_runner.utils.FileUtil import FileUtil

configPath = FileUtil.getAbsolutePath(['resources', 'conf', 'main.yaml'])
appRunner = AppRunner(configPath)
appRunner.run()
