from classes.app.ApplicationRunner import ApplicationRunner

print('Main Program')

appRunner = ApplicationRunner('./conf/main.config.json')

appRunner.run()