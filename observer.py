from abc import ABC, abstractmethod

class Observable:
    def __init__(self):
        self._observer = []
        self._row_added = False

    def add_observer(self, observer):
        if observer not in self._observer:
            self._observer.append(observer)

    def remove_observer(self, observer):
        self._observer.remove(observer)

    def notify_observer(self, row):
        if self.has_added():

            for observer in self._observer:

                observer.notify(row)
        self.clear_changed()

    def clear_changed(self):
        self._row_added = False

    def add_row(self):
        self._row_added = True

    def has_added(self):
        return self._row_added



class Observer(ABC):
    def __init__(self, observable):
        observable.add_observer(self)

    @abstractmethod
    def notify(self, row):
        pass