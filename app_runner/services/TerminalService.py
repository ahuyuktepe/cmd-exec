from xml.etree.ElementTree import ElementTree, Element
from app_runner.services.BaseService import BaseService
from app_runner.ui.classes.TerminalPrintArea import TerminalPrintArea
from app_runner.ui.classes.ViewManager import ViewManager
from app_runner.ui.element.UIView import UIView
from app_runner.ui.utils.UIElementUtil import UIElementBuilder
from app_runner.utils.FileUtil import FileUtil


class TerminalService(BaseService):
    __viewManager: ViewManager

    def __init__(self):
        self.__viewManager = ViewManager()

    def displayView(self, view: UIView):
        if view is not None:
            if self.__viewManager.hasActiveView():
                activeView: UIView = self.__viewManager.getActiveView()
                activeView.clear()
            self.__viewManager.addAndActivateView(view)
            view.display()

    def buildView(self, vid: str) -> UIView:
        # Build Object From Xml
        filePath = FileUtil.getAbsolutePath(['resources', 'terminal', 'views', vid])
        elementTree: ElementTree = FileUtil.generateObjFromFile(filePath + '.xml')
        root: Element = elementTree.getroot()
        # Build View
        view: UIView = UIElementBuilder.buildView(vid, root)
        # Build and Set Printer
        printArea: TerminalPrintArea = TerminalPrintArea()
        printArea.initializeForFullScreen()
        view.setPrintArea(printArea)
        # Build Sections
        sections = self.buildSectionsInView(root, view)
        view.setSections(sections)
        return view

    def buildSectionsInView(self, root: Element, view: UIView) -> list:
        sections: list = []
        sectionElements = root.findall('./section')
        for element in sectionElements:
            section = UIElementBuilder.buildSectionInView(element, view)
            sections.append(section)
        return sections
