from app_runner.menu.Menu import Menu
from app_runner.ui.element import UISection
import math


class UiUtil:
    @staticmethod
    def getCenterMenuElementInSection(menu: Menu, section: UISection) -> UIElement:
        menuWidth = 70
        menuHeight = menu.getCmdCount() * 10
        sectionHeight = section.getHeight()
        sectionWidth = section.getWidth()
        horDiff = math.floor((sectionWidth - menuWidth) / 2)
        verDiff = math.floor((sectionHeight - menuHeight) / 2)
        return UiElement(
            x=horDiff,
            y=verDiff,
            width=menuWidth,
            height=menuHeight,
            obj=menu
        )
