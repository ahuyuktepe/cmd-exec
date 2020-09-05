from app_runner.app.AppRunnerFactory import AppRunnerFactory
from app_runner.app.ApplicationRunner import ApplicationRunner

runner: ApplicationRunner = AppRunnerFactory.buildAppRunner()
runner.run()
