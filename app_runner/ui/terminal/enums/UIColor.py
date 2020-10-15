import curses


class UIColor:
    DEFAULT_MENU_COLOR = 1
    ACTIVE_MENU_COLOR = 2
    ACTIVE_COMMAND_COLOR = 3
    ERROR_MESSAGE_COLOR = 4
    WARNING_MESSAGE_COLOR = 5
    SUCCESS_MESSAGE_COLOR = 6
    INFO_MESSAGE_COLOR = 7

    @staticmethod
    def setColorCodes():
        curses.start_color()
        curses.init_pair(UIColor.DEFAULT_MENU_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(UIColor.ACTIVE_MENU_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(UIColor.ACTIVE_COMMAND_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(UIColor.ERROR_MESSAGE_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(UIColor.WARNING_MESSAGE_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(UIColor.SUCCESS_MESSAGE_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(UIColor.INFO_MESSAGE_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
