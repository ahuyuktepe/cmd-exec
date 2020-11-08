from app_runner.ui.element.UIView import UIView


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

    # Setter Methods

    def addAndActivateView(self, view: UIView):
        self.addView(view)
        self.__activeView = view

    def setActiveView(self, id: str):
        self.__activeView = self.getView(id)
