from app_runner.app.runner.AppRunnerFactory import AppRunnerFactory
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
runner: ApplicationRunner = AppRunnerFactory.buildAppRunner()
runner.run()
