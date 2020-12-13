from app_runner.events.EventManager import EventManager
from app_runner.ui_elements.UIView import UIView


class ViewManager:
    __views: list
    __activeView: UIView

    def __init__(self):
        self.__views = []
        self.__activeView = None

    # Getter Methods

    def addView(self, view: UIView):
        vid = view.getId()
        if not self.hasView(vid):
            self.__views.append(view)

    def getView(self, id: str) -> UIView:
        for view in self.__views:
            if view.getId() == id:
                return view
        return None

    def getActiveView(self) -> UIView:
        return self.__activeView

    def hasActiveView(self) -> bool:
        return self.__activeView is not None

    def hasView(self, id: str) -> bool:
        for view in self.__views:
            if view.getId() == id:
                return True
        return False

    def closeActiveView(self):
        self.__activeView.destroy()
        self.__activeView = None

    # Setter Methods

    def addAndActivateView(self, view: UIView):
        if self.hasActiveView():
            self.__activeView.destroy()
        self.addView(view)
        self.__activeView = view

    def setActiveView(self, id: str):
        self.__activeView = self.getView(id)
