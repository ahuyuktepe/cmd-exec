from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.element import UISection
from app_runner.ui.terminal.element.UIElement import UiElement
import math


class UiUtil:
    @staticmethod
    def getCenterMenuElementInSection(menu: Menu, section: UISection) -> UiElement:
        menuWidth = 70
        menuHeight = menu.getCmdCount() * 10
        sectionHeight = section.getHeight()
        sectionWidth = section.getWidth()
        print('Section Height : ' + str(sectionHeight))
        print('Section Width : ' + str(sectionWidth))
        horDiff = math.floor((sectionWidth - menuWidth) / 2)
        verDiff = math.floor((sectionHeight - menuHeight) / 2)
        return UiElement(
            x=horDiff,
            y=verDiff,
            width=menuWidth,
            height=menuHeight,
            obj=menu
        )
