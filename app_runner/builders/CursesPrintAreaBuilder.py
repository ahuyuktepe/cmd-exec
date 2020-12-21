import curses
from app_runner.builders.PrintAreaBuilder import PrintAreaBuilder
from app_runner.classes.UIPrintArea import UIPrintArea


class CursesPrintAreaBuilder(PrintAreaBuilder):
    __screen: object = None

    def initialize(self):
        self.__screen = curses.initscr()

    def buildPrintArea(self, x: int, y: int, width: int, height: int) -> UIPrintArea:
        window = curses.newwin(height, width, y, x)
        return UIPrintArea(window, x, y, width, height)

    def buildPrintAreaForFullScreen(self) -> UIPrintArea:
        dims: tuple = self.__screen.getmaxyx()
        width = dims[1]
        height = dims[0]
        window = curses.newwin(height, width, 0, 0)
        return UIPrintArea(window, 0, 0, width, height)

    def buildDerivedPrintArea(self, x: int, y: int, width: int, height: int, srcPrintArea: UIPrintArea) -> UIPrintArea:
        window = srcPrintArea.getWindow().derwin(height, width, y, x)
        return UIPrintArea(window, x, y, width, height)
