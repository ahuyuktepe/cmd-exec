from app_runner.classes.UIPrintArea import UIPrintArea


class PrintAreaBuilder:

    def initialize(self):
        pass

    def buildPrintArea(self, x: int, y: int, width: int, height: int) -> UIPrintArea:
        pass

    def buildPrintAreaForFullScreen(self) -> UIPrintArea:
        pass

    def buildDerivedPrintArea(self, x: int, y: int, width: int, height: int, srcPrintArea: UIPrintArea) -> UIPrintArea:
        pass
