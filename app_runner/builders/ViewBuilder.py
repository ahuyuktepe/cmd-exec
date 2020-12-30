from xml.etree.ElementTree import ElementTree, Element
from app_runner.builders.SectionBuilder import SectionBuilder
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.ui_elements.UIView import UIView
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.ValidationUtil import ValidationUtil
from app_runner.utils.XmlElementUtil import XmlElementUtil


class ViewBuilder:
    __sectionBuilder: SectionBuilder

    def __init__(self, sectionBuilder: SectionBuilder):
        self.__sectionBuilder = sectionBuilder

    def buildView(self, printArea: UIPrintArea, vid: str) -> UIView:
        # Generate View File Path
        filePath = self.__generateViewFilePath(vid)
        # Generate Root Xml Element
        root = self.__generateRootXmlElementFromViewId(filePath)
        # Build View
        id = XmlElementUtil.getAttrValueAsStr(root, 'id', vid)
        view: UIView = UIView(id)
        view.setAttributes(root)
        # Build and Set Printer
        view.setPrintArea(printArea)
        # Build Sections
        self.__sectionBuilder.buildSections(root, view)
        return view

    # Private Methods

    def __generateRootXmlElementFromViewId(self, filePath: str) -> Element:
        # Parse Build File
        elementTree: ElementTree = FileUtil.generateObjFromFile(filePath)
        root: Element = elementTree.getroot()
        # Merge Template
        template = XmlElementUtil.getAttrValueAsStr(root, 'template', None)
        if template is not None:
            root = self.__mergeViewIntoTemplate(template, root)
        return root

    def __generateViewFilePath(self, vid) -> str:
        # Set File Path and Verify
        props = StrUtil.getFilePropertiesFromStr(vid)
        fileName = props['file'] + ".view.xml"
        filePath = FileUtil.getAbsolutePath(['modules', props['module'], 'views', fileName])
        ValidationUtil.failIfFileIsNotReadable(filePath, "File '" + filePath + "' to build view is either directory or not readable.")
        return filePath

    def __mergeViewIntoTemplate(self, template: str, viewElement: Element) -> Element:
        # Set File Path and Verify
        props = StrUtil.getFilePropertiesFromStr(template)
        templateFileName = props['file'] + '.template.xml'
        filePath = FileUtil.getAbsolutePath(['modules', props['module'], 'views', templateFileName])
        ValidationUtil.failIfFileIsNotReadable(filePath, "Template file '" + filePath + "' is either directory or not readable.")
        # Build Tree From File
        tempTree: ElementTree = FileUtil.generateObjFromFile(filePath)
        templateRoot = tempTree.getroot()
        # Visit Each Element
        destSections = templateRoot.findall('./section[@ref]')
        for destSection in destSections:
            ref = XmlElementUtil.getAttrValueAsStr(destSection, 'ref', None)
            if ref is not None:
                destSection.set('ref', None)
                srcSections = viewElement.findall("./section[@id='" + ref + "']")
                for srcSection in srcSections:
                    if srcSection.get('hide') == 'true':
                        templateRoot.remove(destSection)
                    XmlElementUtil.removeAllChildren(destSection)
                    XmlElementUtil.copyChildren(srcSection, destSection)
                    XmlElementUtil.overwriteAttributes(srcSection, destSection)
        return templateRoot
