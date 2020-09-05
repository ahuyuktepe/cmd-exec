from app_runner.app.ApplicationRunner import ApplicationRunner


class CmdAppRunner(ApplicationRunner):

    def run(self):
        print('running in cmd mode')
