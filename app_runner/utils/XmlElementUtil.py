import math
from xml.etree.ElementTree import ElementTree, Element


class XmlElementUtil:
    @staticmethod
    def hasAttribute(element: Element, attr: str):
        attributes: dict = element.attrib
        return attributes.get(attr) is not None

    @staticmethod
    def getAttrValueAsStr(element: Element, name: str, default: str = None) -> str:
        attrs: dict = element.attrib
        val = attrs.get(name)
        if val is None:
            return default
        return str(val)

    @staticmethod
    def getAttrValueAsInt(element: Element, name: str, default: int) -> int:
        attrs: dict = element.attrib
        val = attrs.get(name)
        if val is None:
            return default
        return int(val)

    @staticmethod
    def getAttrValueAsBool(element: Element, name: str, default: bool = False) -> bool:
        attrs: dict = element.attrib
        val = attrs.get(name)
        if val is None:
            return default
        valStr = str(val)
        if valStr in ['True', 'true']:
            return True
        return False

    @staticmethod
    def calculateX(element: Element, parentWidth: int, cols: int, colSpan: int) -> int:
        defaultX = 2
        if colSpan <= cols:
            colWidth = math.floor(parentWidth / cols)
            defaultX = (colWidth * (colSpan - 1)) + 2
        return XmlElementUtil.getAttrValueAsInt(element, 'x', defaultX)

    @staticmethod
    def calculateY(element: Element, parentHeight: int, rows: int, rowSpan: int) -> int:
        defaultY = 1
        if rowSpan <= rows:
            rowHeight = math.floor(parentHeight / rows)
            defaultY = (rowHeight * (rowSpan-1)) + 1
        return XmlElementUtil.getAttrValueAsInt(element, 'y', defaultY)

    @staticmethod
    def calculateWidth(element: Element, parentWidth: int, cols: int) -> int:
        colWidth = math.floor(parentWidth / cols)
        return XmlElementUtil.getAttrValueAsInt(element, 'width', colWidth)

    @staticmethod
    def calculateHeight(element: Element, parentHeight: int, rows: int) -> int:
        rowHeight = math.floor(parentHeight / rows)
        return XmlElementUtil.getAttrValueAsInt(element, 'height', rowHeight)

    @staticmethod
    def copyChildren(srcElement: Element, trgElement: Element):
        srcChildren = srcElement.findall('*')
        for child in srcChildren:
            trgElement.append(child)

    @staticmethod
    def overwriteAttributes(srcElement: Element, trgElement: Element):
        attrs: dict = srcElement.attrib
        for key, value in attrs.items():
            trgElement.set(key, value)
