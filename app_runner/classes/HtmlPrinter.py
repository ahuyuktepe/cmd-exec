from xml.etree.ElementTree import ElementTree, Element
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.XmlElementUtil import XmlElementUtil


class HtmlPrinter:
    __printArea: UIPrintArea
    __root: Element
    __y: int
    __start: int
    __end: int
    __maxCharCountPerLine: int

    def __init__(self, html: str, printArea: UIPrintArea):
        self.__printArea = printArea
        self.__root = StrUtil.buildObjFromXmlStr(html)
        self.__maxCharCountPerLine = self.__printArea.getWidth()

    # Getter Methods

    def getY(self) -> int:
        return self.__y

    # Utility Methods

    def printLines(self, start: int, end: int):
        self.__printArea.clear()
        self.__start = start
        self.__end = end
        self.__y = -1
        for element in self.__root:
            if element.tag == 'label':
                self.__printLabel(element)
            elif element.tag == 'p':
                self.__printParagraph(element)
            elif element.tag == 'hr':
                self.__printHorizontalLine(element)
            elif element.tag == 'br':
                self.__y += 1

    # Private Methods
    def __printHorizontalLine(self, element: Element):
        self.__y += 1
        self.__printArea.printLine(0, self.__y, self.__maxCharCountPerLine)

    def __printParagraph(self, element: Element):
        self.__y += 2
        text = "   " + element.text
        lines = StrUtil.splitStrIntoChunks(text, self.__maxCharCountPerLine)
        for line in lines:
            self.__printText(line)
            self.__y += 1
        self.__y -= 1

    def __printLabel(self, label: Element):
        colorCode = XmlElementUtil.getAttrValueAsInt(label, 'data-color', 1)
        self.__y += 1
        text = label.text[:self.__maxCharCountPerLine]
        self.__printText(text, colorCode)

    def __printText(self, text: str, colorCode: int = 1):
        markupStr = ''
        isMarkupOpen = False
        if self.__start <= self.__y < self.__end:
            x = 0
            y = self.__y - self.__start
            for letter in text:
                if letter == '[':
                    isMarkupOpen = True
                    markupStr = ''
                    continue
                elif letter == ']':
                    isMarkupOpen = False
                    continue
                elif isMarkupOpen:
                    markupStr += letter
                    continue
                elif markupStr.startswith('cl:'):
                    arr = markupStr.split(':')
                    colorCode = int(arr[1])
                    markupStr = ''
                    self.__printArea.printText(x, y, letter, colorCode)
                    x += 1
                else:
                    self.__printArea.printText(x, y, letter, colorCode)
                    x += 1
