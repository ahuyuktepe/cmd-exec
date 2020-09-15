import curses

from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil


class UIMenuElement(UIElement):
    _menu: Menu

    def __init__(self, id: str, menu: Menu):
        super().__init__(id, 'menu')
        self._menu = menu

    def getMenu(self) -> Menu:
        return self._menu

    def print(self, window):
        order: int = 1
        x = self.getX()
        y = self.getY()
        width = self.getWidth()
        menu: Menu = self.getMenu()
        idWidth = 10
        bulletPointWidth = 2
        descWidth = self.getWidth() - idWidth - bulletPointWidth

        window.hline((y - 1), x, curses.ACS_HLINE, width)
        window.addstr(y, x, StrUtil.getStrCenterAligned(menu.getName(), width - 2))
        window.hline((y + order), x, curses.ACS_HLINE, width)
        window.vline(y, x, curses.ACS_VLINE, menu.getCmdCount() + 2)
        window.vline(y, (x + width - 1), curses.ACS_VLINE, menu.getCmdCount() + 2)
        cmds = menu.getCommands()
        cmd: Command
        for id, cmd in cmds.items():
            order += 1
            idStr = StrUtil.getStrLeftAligned(id, idWidth)
            descStr = StrUtil.getStrLeftAligned(cmd.getDescription(), descWidth)
            text = '{id}: {desc}'.format(id=idStr, desc=descStr)
            text = StrUtil.getStrCenterAligned(text, self.getWidth())
            window.addstr(
                self.getY() + order,
                self.getX() + 2,
                StrUtil.getStrCenterAligned(text, self.getWidth() - 3)
            )
        order += 1
        window.hline(self.getY() + order, self.getX(), curses.ACS_HLINE, self.getWidth())
