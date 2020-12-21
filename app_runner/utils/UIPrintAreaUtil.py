import curses
from app_runner.classes.UIPrintArea import UIPrintArea


class UIPrintAreaUtil:
    __screen: object = None

    @staticmethod
    def initializeScreen():
        UIPrintAreaUtil.__screen = curses.initscr()

    @staticmethod
    def buildPrintArea(x: int, y: int, width: int, height: int) -> UIPrintArea:
        window = curses.newwin(height, width, y, x)
        return UIPrintArea(window, width, height)

    @staticmethod
    def buildScreenPrintArea() -> UIPrintArea:
        dims: tuple = UIPrintAreaUtil.__screen.getmaxyx()
        width = dims[1]
        height = dims[0]
        window = curses.newwin(height, width, 0, 0)
        return UIPrintArea(window,0, 0, width, height)

    @staticmethod
    def buildDerivedPrintArea(x: int, y: int, width: int, height: int, srcPrintArea: UIPrintArea) -> UIPrintArea:
        window = srcPrintArea.getWindow().derwin(height, width, y, x)
        return UIPrintArea(window, x, y, width, height)

    # ============= Code To Be Enabled ==============

    # @staticmethod
    # def buildPadFullCoverageDerivedPrintArea(srcPrintArea: UIPrintArea) -> UIPrintArea:
    #     width = srcPrintArea.getWidth() - 2
    #     height = srcPrintArea.getHeight() - 2
    #     window = curses.newpad(width, height)
    #     return UIPrintArea(window, width, height)

    # @staticmethod
    # def buildFullCoverageDerivedPrintArea(srcPrintArea: UIPrintArea) -> UIPrintArea:
    #     width = srcPrintArea.getWidth() - 2
    #     height = srcPrintArea.getHeight() - 2
    #     window = srcPrintArea.getWindow().derwin(height, width, 1, 1)
    #     return UIPrintArea(window, 1, 1, width, height)
