from app_runner.ui_elements.UIView import UIView


class ViewManager:
    __views: list
    __activeView: UIView

    def __init__(self):
        self.__views = []
        self.__activeView = None

    # Getter Methods

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

    def addView(self, view: UIView):
        vid = view.getId()
        if not self.hasView(vid):
            self.__views.append(view)

    def activateView(self, view: UIView):
        if view is None:
            raise Exception('Given view is null.')
        elif not self.hasView(view.getId()):
            raise Exception('Given view does not exist in view list.')
        elif self.hasActiveView():
            self.__activeView.destroy()
        self.__activeView = view

    def setActiveView(self, id: str):
        self.__activeView = self.getView(id)

    # ============= Code To Be Enabled ==============

    # def closeActiveView(self):
    #     self.__activeView.destroy()
    #     self.__activeView = None
