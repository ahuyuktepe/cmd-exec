from classes.app.ApplicationConfig import ApplicationConfig

class ApplicationRunner:
    __appConfig: ApplicationConfig

    def __init__(self, configPath: str):
        self.__appConfig = ApplicationConfig(configPath)

    def run(self):
        print('Run')
        value: int = self.__appConfig.getIntValue('a.b')
        print('Value : {value}'.format(value= value))
