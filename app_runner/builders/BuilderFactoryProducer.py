from app_runner.builders.BuilderFactory import BuilderFactory
from app_runner.builders.CursesBuilderFactory import CursesBuilderFactory


class BuilderFactoryProducer:

    @staticmethod
    def getFactory(type: str) -> BuilderFactory:
        if type == 'curses':
            return CursesBuilderFactory()
        return None
