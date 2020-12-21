import math
from xml.etree.ElementTree import ElementTree, Element
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.enums.UIColor import UIColor
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.XmlElementUtil import XmlElementUtil


class XmlPrinter:
    __printArea: UIPrintArea
    __root: Element
    __lines: dict
    __y: int
    __maxCharCountPerLine: int

    def __init__(self, xmlStr: str, printArea: UIPrintArea):
        self.__printArea = printArea
        self.__root = StrUtil.buildObjFromXmlStr(xmlStr)
        self.__lines = {}
        self.__maxCharCountPerLine = self.__printArea.getWidth() - 2
        self.__buildLines()

    # Getter Methods

    def hasLine(self, lineNo: int) -> bool:
        lineProps = self.__lines.get(lineNo)
        return lineProps is not None

    # Utility Methods

    def printLine(self, lineNo: int, y: int):
        if self.hasLine(lineNo):
            lineProps = self.__lines.get(lineNo)
            for props in lineProps:
                self.__printArea.printText(props['x'], y, props['text'], props['color'])

    # Private Methods

    def __buildLines(self):
        self.__y = -1
        for element in self.__root:
            if element.tag == 'ul':
                self.__printOrderedList(element)
            elif element.tag == 'table':
                self.__printTable(element)
            elif element.tag == 'grid':
                self.__printGrid(element)
            elif element.tag == 'hr':
                self.__printHorizontalLine()
            elif element.tag == 'p':
                self.__printParagraph(element)
            elif element.tag == 'label':
                self.__printLabel(element)
            elif element.tag == 'br':
                self.__printBreakLine(element)

    def __printBreakLine(self, element: Element):
        lineCount = XmlElementUtil.getAttrValueAsInt(element, 'lines', 1)
        for i in range(1, lineCount):
            self.__y += 1
            self.__addLine(1, self.__y, '')

    def __printLabel(self, element: Element):
        colorCode = XmlElementUtil.getAttrValueAsInt(element, 'color', 1)
        self.__y += 1
        text = element.text[:self.__maxCharCountPerLine]
        self.__addLine(1, self.__y, text, colorCode)

    def __printParagraph(self, element: Element):
        self.__y += 2
        text = "   " + element.text
        text = text.strip()
        lines = StrUtil.splitStrIntoChunks(text, self.__maxCharCountPerLine)
        for line in lines:
            line = line.replace('\n', '').strip(' ')
            self.__addLine(1, self.__y, line)
            self.__y += 1

    def __printHorizontalLine(self):
        lineText = '-' * (self.__maxCharCountPerLine - 1)
        self.__addLine(1, self.__y, lineText)

    def __printOrderedList(self, element: Element, x: int = 1):
        bulletPointChar = XmlElementUtil.getAttrValueAsStr(element, 'char', '*')
        spaceCount = XmlElementUtil.getAttrValueAsInt(element, 'indentation', 3)
        indentation = ' ' * spaceCount
        self.__y += 1
        items = element.findall('./li')
        for item in items:
            text = indentation + bulletPointChar + ' ' + item.text
            text = StrUtil.getAlignedAndLimitedStr(text, 15, 'left')
            self.__addLine(x, self.__y, text)
            subOrderedListItem = item.find('ul')
            if subOrderedListItem is not None:
                self.__printOrderedList(subOrderedListItem, x + spaceCount)
            else:
                self.__y += 1

    def __printTable(self, element: Element):
        x = 1
        self.__addLine(x, self.__y, '')
        self.__y += 1
        # Print Headers
        cols = element.findall("./tr/th")
        colWidth = math.floor(self.__maxCharCountPerLine / len(cols))
        for col in cols:
            text = StrUtil.getAlignedAndLimitedStr(col.text, colWidth, 'left')
            self.__addLine(x, self.__y, text, UIColor.ACTIVE_MENU_COLOR)
            x += colWidth
        # Print Data
        rows = element.findall("./tr")
        for row in rows:
            cols = row.findall('./td')
            for col in cols:
                text = StrUtil.getAlignedAndLimitedStr(col.text, colWidth, 'left')
                self.__addLine(x, self.__y, text)
                x += colWidth
            self.__y += 1
            x = 1

    def __printGrid(self, element: Element):
        x = 1
        self.__addLine(x, self.__y, '')
        self.__y += 1
        rows = element.findall("./row")
        for row in rows:
            cols = row.findall('./col')
            for col in cols:
                label = col.find('label')
                value = col.find('value')
                labelText = StrUtil.getAlignedAndLimitedStr(label.text, 15, 'left')
                self.__addLine(x, self.__y, labelText, UIColor.TABLE_HEADER_COLOR)
                x += len(labelText)
                self.__addLine(x, self.__y, ":", UIColor.TABLE_HEADER_COLOR)
                x += 2
                valueText = StrUtil.getAlignedAndLimitedStr(value.text, 15, 'left')
                self.__addLine(x, self.__y, valueText)
                x += len(valueText)
            self.__y += 1
            x = 1

    def __addLine(self, x: int, y: int, text: str, color: int = 1):
        lineProps = self.__lines.get(y)
        if lineProps is None:
            lineProps = []
        lineProps.append({
            "x": x,
            "y": y,
            "text": text,
            "color": color
        })
        self.__lines[y] = lineProps
