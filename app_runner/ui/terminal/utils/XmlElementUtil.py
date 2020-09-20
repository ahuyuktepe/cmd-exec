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
    def isAttrTrue(element: Element, name: str, default: bool = True) -> bool:
        attrs: dict = element.attrib
        val = str(attrs.get(name))
        if val is None:
            return default
        return val == 'True' or val == 'true' or val == '1'
