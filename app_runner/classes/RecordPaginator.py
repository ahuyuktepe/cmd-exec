import math


class RecordPaginator:
    __page: int
    __recordCountPerPage: int
    __recordsInPage: list
    __totalPageCount: int
    __records: list
    __totalRecordCount: int
    __activeIndex: int

    def __init__(self, records: list, recordCountPerPage: int):
        self.__page = 1
        self.__recordCountPerPage = recordCountPerPage
        self.__records = records
        self.__totalRecordCount = len(self.__records)
        self.__activeIndex = -1
        self.__recordsInPage = self.__getRecordsInPage()
        self.__totalPageCount = math.ceil(self.__totalRecordCount / self.__recordCountPerPage)

    # Private Methods

    def __getRecordsInPage(self) -> list:
        fromIndex = (self.__page - 1) * self.__recordCountPerPage
        toIndex = fromIndex + self.__recordCountPerPage
        if toIndex > self.__totalRecordCount:
            toIndex = self.__totalRecordCount
        return self.__records[fromIndex:toIndex]

    # Setter Methods

    def setActiveIndex(self, index: int):
        self.__activeIndex = index

    # Getter Methods

    def getRecordCountInCurrentPage(self) -> int:
        return len(self.__recordsInPage)

    def getActiveRecord(self) -> object:
        return self.__recordsInPage[self.__activeIndex]

    def getRecordsInPage(self) -> list:
        return self.__recordsInPage

    def getActiveIndex(self) -> int:
        return self.__activeIndex

    def printDetails(self):
        print('page: ' + str(self.__page) + ' | recordCountPerPage: ' + str(self.__recordCountPerPage) +
              ' | records: ' + str(self.__records) + ' | totalRecordCount: ' + str(self.__totalRecordCount) +
              ' | activeIndex: ' + str(self.__activeIndex) + ' | recordsInPage: ' + str(self.__recordsInPage) +
              ' | totalPageCount: ' + str(self.__totalPageCount))

    # Utility Methods

    def hasNextPage(self) -> bool:
        return self.__page < self.__totalPageCount

    def hasPreviousPage(self) -> bool:
        return self.__page > 1

    def moveToNextPage(self):
        if self.hasNextPage():
            self.__page += 1
            self.__recordsInPage = self.__getRecordsInPage()

    def moveToPreviousPage(self):
        if self.hasPreviousPage():
            self.__page -= 1
            self.__recordsInPage = self.__getRecordsInPage()

    def isLastRecordInPage(self) -> bool:
        return self.__activeIndex == len(self.__recordsInPage) - 1

    def isLastRecordOnLastPage(self):
        return self.isLastRecordInPage() and self.isOnLastPage()

    def isOnLastPage(self):
        return self.__page == self.__totalPageCount

    def isFirstRecordInPage(self) -> bool:
        return self.__activeIndex == 0

    def isFirstRecordOnFirstPage(self):
        return self.isFirstRecordInPage() and self.isOnFirstPage()

    def isOnFirstPage(self):
        return self.__page == 1

    def moveToNextRecord(self):
        if self.isLastRecordInPage():
            if self.hasNextPage():
                self.__activeIndex = 0
                self.moveToNextPage()
        else:
            self.__activeIndex += 1

    def moveToPreviousRecord(self):
        if self.isFirstRecordInPage():
            if self.hasPreviousPage():
                self.__activeIndex = self.__recordCountPerPage - 1
                self.moveToPreviousPage()
        else:
            self.__activeIndex -= 1
