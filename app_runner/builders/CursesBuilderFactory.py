from app_runner.builders.BuilderFactory import BuilderFactory
from app_runner.builders.CursesPrintAreaBuilder import CursesPrintAreaBuilder
from app_runner.builders.ElementBuilder import ElementBuilder
from app_runner.builders.PrintAreaBuilder import PrintAreaBuilder
from app_runner.builders.SectionBuilder import SectionBuilder
from app_runner.builders.ViewBuilder import ViewBuilder


class CursesBuilderFactory(BuilderFactory):

    def getViewBuilder(self) -> ViewBuilder:
        sectionBuilder = self.getSectionBuilder()
        return ViewBuilder(sectionBuilder)

    def getSectionBuilder(self) -> SectionBuilder:
        elementBuilder = self.getElementBuilder()
        printAreaBuilder = self.getPrintAreaBuilder()
        return SectionBuilder(elementBuilder, printAreaBuilder)

    def getElementBuilder(self) -> ElementBuilder:
        printAreaBuilder = self.getPrintAreaBuilder()
        return ElementBuilder(printAreaBuilder)

    def getPrintAreaBuilder(self) -> PrintAreaBuilder:
        return CursesPrintAreaBuilder()
