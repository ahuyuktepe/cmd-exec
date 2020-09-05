from app_runner.app.ApplicationRunner import ApplicationRunner


class IntAppRunner(ApplicationRunner):

    def run(self):
        print('running in interactive mode')
