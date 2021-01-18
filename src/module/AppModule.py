from src.module.ModuleDependency import ModuleDependency


class AppModule:
    __name: str
    __description: str
    __version: str
    __dependencies: list

    def __init__(self, name: str, version: str, description: str = None):
        self.__name = name
        self.__description = description
        self.__version = version
        self.__dependencies = []

    # Getter Methods

    def getName(self) -> str:
        return self.__name

    def getDescription(self) -> str:
        return self.__description

    def getVersion(self) -> str:
        return self.__version

    def getDependencies(self) -> list:
        return self.__dependencies

    # Setter Methods

    def addDependency(self, depStr: str):
        dependency = ModuleDependency(depStr)
        self.__dependencies.append(dependency)
