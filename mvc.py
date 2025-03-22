from abc import abstractmethod


class Model:


    def __init__(self):
        self.rows = []

    @abstractmethod
    def add_row(self, row):
        """Add a row to the model."""
        pass

    def get_rows(self):
        """Get all rows from the model."""
        return self.rows

class View:

    @abstractmethod
    def show_data(self, rows):
        """Display data in the view."""
        pass

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add_row(self, row):
        """Add a row to the model and update the view."""
        self.model.add_row(row)
        self.update_view()

    def update_view(self):
        """Update the view with the model data."""
        rows = self.model.get_rows()
        self.view.show_data(rows)

if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)
