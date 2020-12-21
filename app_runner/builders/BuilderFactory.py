from app_runner.builders.ElementBuilder import ElementBuilder
from app_runner.builders.PrintAreaBuilder import PrintAreaBuilder
from app_runner.builders.SectionBuilder import SectionBuilder
from app_runner.builders.ViewBuilder import ViewBuilder


class BuilderFactory:

    def getViewBuilder(self) -> ViewBuilder:
        pass

    def getSectionBuilder(self) -> SectionBuilder:
        pass

    def getElementBuilder(self) -> ElementBuilder:
        pass

    def getPrintAreaBuilder(self) -> PrintAreaBuilder:
        pass
