from app_runner.app.ApplicationRunner import ApplicationRunner
from app_runner.app.CmdAppRunner import CmdAppRunner
from app_runner.app.IntAppRunner import IntAppRunner
from app_runner.services.ArgumentService import ArgumentService


class AppRunnerFactory:

    @staticmethod
    def buildAppRunner() -> ApplicationRunner:
        argumentService = ArgumentService()
        if argumentService.isCmdMode():
            return AppRunnerFactory.buildCmdRunner()
        elif argumentService.isInteractiveMode():
            return AppRunnerFactory.buildInteractiveRunner()

    @staticmethod
    def buildCmdRunner() -> CmdAppRunner:
        return CmdAppRunner()

    @staticmethod
    def buildInteractiveRunner() -> IntAppRunner:
        return IntAppRunner()
