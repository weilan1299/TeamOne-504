
from mvc import Model

from mvc import Controller
import unittest
from unittest.mock import MagicMock, patch


from Tkinter import *





# Concrete implementations for testing
class ConcreteModel(Model):
    def add_row(self, row):
        self.rows.append(row)


class ConcreteView(View):
    def show_data(self, rows):
        self.rows = rows


# Test cases
class TestController(unittest.TestCase):

    def setUp(self):
        # Create concrete model and view for testing
        self.model = ConcreteModel()
        self.view = ConcreteView()
        self.controller = Controller(self.model, self.view)

    def test_add_row(self):
        # Test adding a row to the model through the controller
        self.controller.add_row("row1")

        # Check that the model has the row
        self.assertIn("row1", self.model.get_rows())

        # Check that the view's show_data was called with the correct data
        self.assertEqual(self.view.rows, self.model.get_rows())

    def test_multiple_rows(self):
        # Test adding multiple rows
        self.controller.add_row("row1")
        self.controller.add_row("row2")

        # Check that the model contains both rows
        self.assertIn("row1", self.model.get_rows())
        self.assertIn("row2", self.model.get_rows())

        # Check that the view's show_data was called with the updated rows
        self.assertEqual(self.view.rows, self.model.get_rows())

    def test_view_update_on_add_row(self):
        # Create a mock for view to ensure show_data is called with the correct argument
        self.view.show_data = MagicMock()

        self.controller.add_row("row1")

        # Check that the view's show_data method was called with the updated rows
        self.view.show_data.assert_called_with(["row1"])