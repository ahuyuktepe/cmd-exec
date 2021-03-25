from cmd_exec.util.FileUtil import FileUtil


class AppUtil:

    @staticmethod
    def getMainConfig() -> dict:
        path = ['resources', 'configs', 'main.config.yaml']
        if FileUtil.doesFileExist(path):
            return FileUtil.generateObjFromYamlFile(path)
        return {}

    @staticmethod
    def getDefaultConfig() -> dict:
        return {
            'application': {
                'name': 'Command Executor',
                'modes': [
                    {'id': 'cmd', 'runner': 'CoreCmdExecApp'}
                ]
            }
        }
