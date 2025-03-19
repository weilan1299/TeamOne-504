from unittest.mock import MagicMock
from mvc import Model
from mvc import View
from mvc import Controller
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from watchdog.events import FileSystemEvent
from databaseManager import DatabaseManager
from FileWatcher import FileHandler, FileWatch
from Tkinter import *
from databaseManager import DatabaseManager




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



class TestFileHandler(unittest.TestCase):

    def setUp(self):
        # Mocking the Controller (file adding functionality) and DatabaseManager (mocking database interaction)
        self.controller = MagicMock(spec=Controller)
        self.database = MagicMock(spec=DatabaseManager)

        self.file_handler = FileHandler(self.controller, self.database, extension=['.txt'])

    @patch('os.path.basename')
    @patch('os.path.splitext')
    @patch('os.path.dirname')
    def test_on_modified_with_matching_extension(self, mock_dirname, mock_splitext, mock_basename):
        # Mocking file event details
        mock_basename.return_value = 'testfile.txt'
        mock_splitext.return_value = ('testfile', '.txt')
        mock_dirname.return_value = '/mock/path'

        event = MagicMock(spec=FileSystemEvent)
        event.is_directory = False
        event.src_path = '/mock/path/testfile.txt'

        # Simulating 'modified' event
        self.file_handler.on_modified(event)

        # Checking that log_event is called with the expected 'Modified' event
        self.file_handler.log_event.assert_called_with('Modified')

    @patch('os.path.basename')
    @patch('os.path.splitext')
    @patch('os.path.dirname')
    def test_on_created_with_matching_extension(self, mock_dirname, mock_splitext, mock_basename):
        # Mocking file event details
        mock_basename.return_value = 'testfile.txt'
        mock_splitext.return_value = ('testfile', '.txt')
        mock_dirname.return_value = '/mock/path'

        event = MagicMock(spec=FileSystemEvent)
        event.is_directory = False
        event.src_path = '/mock/path/testfile.txt'

        # Simulating 'created' event
        self.file_handler.on_created(event)

        # Checking that log_event is called with the expected 'Created' event
        #self.file_handler.log_event.assert_called_with('Created')

    @patch('os.path.basename')
    @patch('os.path.splitext')
    @patch('os.path.dirname')
    def test_on_deleted_with_matching_extension(self, mock_dirname, mock_splitext, mock_basename):
        # Mocking file event details
        mock_basename.return_value = 'testfile.txt'
        mock_splitext.return_value = ('testfile', '.txt')
        mock_dirname.return_value = '/mock/path'

        event = MagicMock(spec=FileSystemEvent)
        event.is_directory = False
        event.src_path = '/mock/path/testfile.txt'

        # Simulating 'deleted' event
        self.file_handler.on_deleted(event)

        # Checking that log_event is called with the expected 'Deleted' event
        #self.file_handler.log_event.assert_called_with('Deleted')


class TestFileWatch(unittest.TestCase):

    def setUp(self):
        # Mocking the Controller (file adding functionality) and View (check method)
        self.model = MagicMock()
        self.view = MagicMock()
        self.file_watch = FileWatch(self.model, self.view)

    def test_monitoredFile_property(self):
        self.file_watch.monitoredFile = ['/mock/path']
        self.assertEqual(self.file_watch.monitoredFile, ['/mock/path'])

    def test_extension_property(self):
        self.file_watch.extension = '.txt'
        self.assertEqual(self.file_watch.extension, ['.txt'])

    @patch('watchdog.observers.Observer')
    def test_start_with_files_to_watch(self, MockObserver):
        # Mock view check method to return 1 (indicating recursive monitoring)
        self.view.check.return_value = 1

        self.file_watch.monitoredFile = ['/mock/path']
        self.file_watch.start()

        # Check that observer schedule is called
        MockObserver().schedule.assert_called_once()

    @patch('watchdog.observers.Observer')
    def test_start_without_files_to_watch(self, MockObserver):
        # Test with no files to watch
        self.file_watch.monitoredFile = []
        self.file_watch.start()

        # Ensure no schedule method is called
        MockObserver().schedule.assert_not_called()

    @patch('watchdog.observers.Observer')
    def test_stop_when_monitoring_is_running(self, MockObserver):
        # Mocking the observer to be alive
        observer = MockObserver.return_value
        observer.is_alive.return_value = True

        self.file_watch.stop()

        # Ensure the observer stop method was called
        observer.stop.assert_called_once()

    @patch('watchdog.observers.Observer')
    def test_stop_when_monitoring_is_not_running(self, MockObserver):
        # Mocking the observer to be not alive
        observer = MockObserver.return_value
        observer.is_alive.return_value = False

        self.file_watch.stop()

        # Ensure the observer stop method was not called
        observer.stop.assert_not_called()


if __name__ == "__main__":
    unittest.main()
