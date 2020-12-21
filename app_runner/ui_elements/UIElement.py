from xml.etree.ElementTree import Element
from app_runner.classes import UIPrintArea
from app_runner.errors.AppRunnerError import AppRunnerError
from app_runner.utils.StrUtil import StrUtil


class UIElement:
    _id: str
    _type: str
    _printArea: UIPrintArea

    def __init__(self, id: str, type: str):
        self._id = id
        self._type = type
        self._withBorder = False

    # Getter Functions

    def getId(self) -> str:
        return self._id

    def getType(self) -> str:
        return self._type

    def getX(self) -> int:
        return self._printArea.getX()

    def getY(self) -> int:
        return self._printArea.getY()

    def getWidth(self) -> int:
        return self._printArea.getWidth()

    def getHeight(self) -> int:
        return self._printArea.getHeight()

    def getPrintArea(self) -> UIPrintArea:
        return self._printArea

    # Setter Methods

    def setAttributes(self, element: Element):
        pass

    def setPrintArea(self, printArea: UIPrintArea):
        self._printArea = printArea

    # Flow Methods

    def listenEvents(self):
        pass

    def display(self):
        pass

    def destroy(self):
        self._printArea.clear()
        self._printArea.refresh()

    def initialize(self):
        pass

    def clear(self):
        self._printArea.clear()

    def refresh(self):
        self._printArea.refresh()

    # Utility Methods

    def print(self, x: int, y: int, text: str, colorCode: int = 0):
        if y > self.getHeight():
            msg = "{type} type element '{id}' y value '{y}' is is greater than max allowable y '{maxY}'.".format(
                    type=self.getType(),
                    id=self.getId(),
                    y=str(y),
                    maxY=str(self.getHeight())
            ).capitalize()
            raise AppRunnerError(msg)
        arr = StrUtil.parseColoredText(text, colorCode)
        self._printArea.printText(x, y, arr['text'], arr['colorCode'])

    # ============= Code To Be Enabled ==============

    # def isSelectable(self) -> bool:
    #     return True
    #
    # def focus(self):
    #     pass
    #
    # def unfocus(self):
    #     pass
