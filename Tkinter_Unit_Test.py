import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import Menu
import customtkinter
from Tkinter import Tkinter_GUI  # Assuming the class is in tkinter_gui.py


class TestTkinterGUI(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.root = tk.Tk()
        self.gui = Tkinter_GUI(self.root)

    @patch('tkinter.Tk')
    def test_initialization(self, mock_root):
        """Test that the main window and some widgets are initialized."""
        self.assertEqual(self.gui.root.title(), "File System Watcher")
        self.assertIsNotNone(self.gui.monitor)
        self.assertIsNotNone(self.gui.databaseManager)
        self.assertIsInstance(self.gui.menubar, Menu)

    @patch('filewatch.FileWatch')  # Mocking FileWatch
    def test_start_monitoring(self, FileWatcher):
        """Test the 'Start Watching' menu item action."""
        mock_monitor = MagicMock()
        FileWatcher.return_value = mock_monitor

        # Simulate clicking on 'Start Watching' menu item
        self.gui.start_monitoring()

        # Verify that the start_monitoring method triggered the correct actions
        mock_monitor.start_monitoring.assert_called_once()

    @patch('filewatch.FileWatch')  # Mocking FileWatch
    def test_stop_monitoring(self, FileWatcher):
        """Test the 'Stop Watching' menu item action."""
        mock_monitor = MagicMock()
        FileWatcher.return_value = mock_monitor

        # Simulate clicking on 'Stop Watching' menu item
        self.gui.stop_monitoring()

        # Verify that the stop_monitoring method was called
        mock_monitor.stop_monitoring.assert_called_once()

    @patch('filewatch.FileWatch')  # Mocking FileWatch
    def test_reset(self, FileWatcher):
        """Test the 'Reset' menu item action."""
        mock_monitor = MagicMock()
        FileWatcher.return_value = mock_monitor

        # Simulate clicking on 'Reset' menu item
        self.gui.reset()

        # Verify reset logic (if implemented)
        mock_monitor.reset.assert_called_once()

    @patch('filewatch.FileWatch')  # Mocking FileWatch
    def test_db_write(self, FileWatcher):
        """Test the 'Write' database action."""
        mock_monitor = MagicMock()
        FileWatcher.return_value = mock_monitor

        # Simulate clicking on 'Write' database action
        self.gui.db_write()

        # Verify that the write action calls the corresponding database method
        mock_monitor.databaseManager.write.assert_called_once()

    @patch('filewatch.FileWatch')  # Mocking FileWatch
    def test_db_clear(self, FileWatcher):
        """Test the 'Clear database' action."""
        mock_monitor = MagicMock()
        FileWatcher.return_value = mock_monitor

        # Simulate clicking on 'Clear database' menu item
        self.gui.db_clear()

        # Verify that the clear method was called
        mock_monitor.databaseManager.clear.assert_called_once()

    @patch('filewatch.FileWatch')  # Mocking FileWatch
    def test_query_window(self, FileWatcher):
        """Test the 'Query' menu item action."""
        mock_monitor = MagicMock()
        FileWatcher.return_value = mock_monitor

        # Simulate clicking on 'Query' menu item
        self.gui.query_window()

        # Verify that the query method opens the query window
        self.assertTrue(self.gui.query_window_called)

    @patch('tkinter.filedialog.askdirectory')  # Mocking the file dialog
    def test_open_directory(self, mock_askdirectory):
        """Test the 'Browse for directory to watch' action."""
        # Simulate a directory being selected
        mock_askdirectory.return_value = "/some/directory"

        # Simulate clicking on 'Browse for directory' menu item
        self.gui.open_directory()

        # Verify the method that uses the directory path is called correctly
        self.assertEqual(self.gui.path.get(), "/some/directory")

    def tearDown(self):
        """Clean up after each test."""
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
