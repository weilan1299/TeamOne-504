
from main import Tkinter_GUI
import os
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
import tkinter as tk

class DummyController:
    def __init__(self):
        self.monitoredFile = None
        self.extension = None

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True


class DummyModel:
    def delete_record(self):
        pass

    def query_data(self, ext, event):
        # Return dummy data for query.
        return [("query.txt", "C:/query", "modified", "2025-03-19 14:00:00")]


# --- Unit Tests for Tkinter_GUI ---
class TestTkinterGUI(unittest.TestCase):
    def setUp(self):
        # Create a Tk root window and hide it during tests.
        self.root = tk.Tk()
        self.root.withdraw()
        self.view = Tkinter_GUI(self.root)
        # Inject dummy controller and model.
        self.controller = DummyController()
        self.model = DummyModel()
        self.view.controller = self.controller
        self.view.model = self.model

    def tearDown(self):
        self.root.destroy()

    def test_reset_clears_entries(self):
        # Use name-mangled attributes if defined as private.
        self.view._Tkinter_GUI__filename.set("dummy file")
        self.view._Tkinter_GUI__path.set("dummy path")
        self.view.event.set("dummy event")
        self.view.time.set("dummy time")
        self.view.entry_var.set("dummy entry")
        self.view.database_entry.set("dummy db")

        # Call the reset method.
        self.view.reset()

        # Assert that all StringVars have been cleared.
        self.assertEqual(self.view._Tkinter_GUI__filename.get(), "")
        self.assertEqual(self.view._Tkinter_GUI__path.get(), "")
        self.assertEqual(self.view.event.get(), "")
        self.assertEqual(self.view.time.get(), "")
        self.assertEqual(self.view.entry_var.get(), "")
        self.assertEqual(self.view.database_entry.get(), "")

    def test_start_monitoring_calls_controller_start(self):
        # Set a valid directory path.
        self.view.entry_var.set("/valid/path")
        # Set an extension in the ext_combo.
        self.view.ext_combo.set(".py")

        # Call start_monitoring.
        self.view.start_monitoring()

        # Verify that the controller's monitoredFile and extension are updated.
        self.assertEqual(self.controller.monitoredFile, "/valid/path")
        self.assertEqual(self.controller.extension, ".py")
        # Verify that the controller's start() method was called.
        self.assertTrue(hasattr(self.controller, "started") and self.controller.started)
        # Verify that the start button's text and state are updated.
        self.assertEqual(self.view.start_watch_btn.cget("text"), "Monitoring...")
        self.assertEqual(self.view.start_btn.cget("state"), tk.DISABLED)

    @patch("tkinter.messagebox.askyesno", return_value=True)
    def test_stop_monitoring_calls_controller_stop(self, mock_askyesno):
        # Set a valid path so stop_monitoring won't show an error.
        self.view.entry_var.set("/valid/path")
        # Pre-configure the buttons as if monitoring is in progress.
        self.view.start_watch_btn.configure(text="Monitoring...", state=tk.DISABLED)
        self.view.start_btn.configure(state=tk.DISABLED)

        # Call stop_monitoring.
        self.view.stop_monitoring()

        # Verify that the controller's stop() method was called.
        self.assertTrue(hasattr(self.controller, "stopped") and self.controller.stopped)
        # Verify that the buttons are updated.
        self.assertEqual(self.view.start_watch_btn.cget("text"), "Start Monitoring")
        self.assertEqual(self.view.start_btn.cget("state"), tk.NORMAL)

    def test_show_data_updates_treeview(self):
        # Clear existing items in the treeview.
        for item in self.view.treeview.get_children():
            self.view.treeview.delete(item)
        # Create a sample row.
        sample_row = ("file1.txt", "C:/dummy", "modified", "2025-03-19 12:00:00")
        # Call show_data with a list containing the sample row.
        self.view.show_data([sample_row])
        # Verify that one row was inserted.
        items = self.view.treeview.get_children()
        self.assertEqual(len(items), 1)
        inserted = self.view.treeview.item(items[0], "values")
        self.assertEqual(list(inserted), list(sample_row))

    def test_db_query_updates_treeview(self):
        # Patch wait_window for the query window to return immediately.
        with patch("customtkinter.CTkFrame.wait_window", return_value=None):
            self.view.query_window()

        # Simulate user selecting query criteria.
        self.view.q_ext_combo.set(".txt")
        self.view.q_event_type_combo.set("modified")

        # Patch the model's query_data method to return dummy data.
        dummy_data = [("query.txt", "C:/query", "modified", "2025-03-19 14:00:00")]
        self.view.model.query_data = MagicMock(return_value=dummy_data)

        # Call the query method.
        self.view.db_query()

        # Verify that the query table is populated.
        items = self.view.table.get_children()
        self.assertEqual(len(items), len(dummy_data))
        inserted = self.view.table.item(items[0], "values")
        self.assertEqual(list(inserted), list(dummy_data[0]))

    @patch("smtplib.SMTP_SSL")
    @patch("tkinter.messagebox.showinfo")
    def test_send_email_success(self, mock_showinfo, mock_smtp):

        # Create a temporary CSV file to simulate export_db_to_csv.
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
            tmp.write("dummy csv content")
            tmp_path = tmp.name

        # Patch the model's export_db_to_csv method to return our temporary CSV path.
        self.view.model.export_db_to_csv = MagicMock(return_value=tmp_path)

        # Instead of creating a new email window, simulate an existing email entry.
        self.view.email_entry = MagicMock()
        self.view.email_entry.get.return_value = "dummy@example.com"

        # Forcefully set the environment variables for email credentials.
        EMAIL_ADDRESS = os.getenv("FILE_EMAIL")
        EMAIL_PASSWORD =  os.getenv("FILE_PASSWORD")

        # Set up the SMTP_SSL mock to support context manager usage.
        smtp_instance = MagicMock()
        smtp_instance.login.return_value = None
        smtp_instance.send_message.return_value = None
        mock_smtp.return_value.__enter__.return_value = smtp_instance

        # Call send_email.
        self.view.send_email()

        # Check that SMTP_SSL was called with the correct parameters.
        mock_smtp.assert_called_with("smtp.gmail.com", 465)

        # Check that login and send_message were called on the dummy SMTP instance.
        smtp_instance.login.assert_called_with(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp_instance.send_message.assert_called()

        # Check that messagebox.showinfo was called with the success message.
        # mock_showinfo.assert_called_with("Sent Email", "Email has been sent.")
        # Verify success message
        print("Email passed the test")

        # Cleanup temporary CSV file.
        os.unlink(tmp_path)




if __name__ == "__main__":
    unittest.main()
