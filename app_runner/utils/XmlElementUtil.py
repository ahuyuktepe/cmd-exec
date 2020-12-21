import math
from xml.etree.ElementTree import Element


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
    def removeAllChildren(element: Element):
        srcChildren = element.findall('*')
        for child in srcChildren:
            element.remove(child)

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

    @staticmethod
    def calculateElementX(x: str, sectionWidth: int, defaultX: int = 1) -> int:
        if x is None:
            return defaultX
        elif x.startswith('-'):
            return sectionWidth - int(x[1:])
        elif x.startswith('/'):
            return math.floor(sectionWidth / int(x[1:]))
        else:
            return int(x)

    @staticmethod
    def calculateElementY(y: str, sectionHeight: int, defaultY: int = 1) -> int:
        if y is None:
            return defaultY
        elif y.startswith('-'):
            return sectionHeight - int(y[1:])
        elif y.startswith('/'):
            return math.floor(sectionHeight / int(y[1:]))
        else:
            return int(y)

    # ============= Code To Be Enabled ==============

    # @staticmethod
    # def calculateY(element: Element, parentHeight: int, rows: int, rowSpan: int) -> int:
    #     defaultY = 1
    #     if rowSpan <= rows:
    #         rowHeight = math.floor(parentHeight / rows)
    #         defaultY = (rowHeight * (rowSpan-1)) + 1
    #     return XmlElementUtil.getAttrValueAsInt(element, 'y', defaultY)

    # @staticmethod
    # def calculateWidth(element: Element, parentWidth: int, cols: int) -> int:
    #     colWidth = math.floor(parentWidth / cols)
    #     return XmlElementUtil.getAttrValueAsInt(element, 'width', colWidth)

    # @staticmethod
    # def calculateHeight(element: Element, parentHeight: int, rows: int) -> int:
    #     rowHeight = math.floor(parentHeight / rows)
    #     return XmlElementUtil.getAttrValueAsInt(element, 'height', rowHeight)
