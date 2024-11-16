
import sys
import unittest
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QProgressBar, QTextEdit
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt
import logging
import datetime
import os

# -----------------------------------------------------------------------------------------------------
# @ QT6 Test Runner Interface
# -----------------------------------------------------------------------------------------------------

class TestRunnerInterface(QMainWindow):
    """
    A Qt6-based GUI to run and visualize unit tests, providing a detailed log view and progress overview.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Test Runner")
        self.setGeometry(100, 100, 800, 600)

        # Setup main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # UI Elements
        self.test_list = QListWidget()
        self.run_tests_button = QPushButton("Run Selected Tests")
        self.progress_bar = QProgressBar()
        self.log_viewer = QTextEdit()

        # Configure UI Elements
        self.run_tests_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.log_viewer.setReadOnly(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to layout
        self.layout.addWidget(QLabel("Select Tests to Run:"))
        self.layout.addWidget(self.test_list)
        self.layout.addWidget(self.run_tests_button)
        self.layout.addWidget(QLabel("Progress:"))
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(QLabel("Test Log Output:"))
        self.layout.addWidget(self.log_viewer)

        # Signals and Slots
        self.run_tests_button.clicked.connect(self.run_tests)

        # Load Tests
        self.load_tests()

    def load_tests(self):
        """
        Load the available test cases and populate the QListWidget.
        """
        self.log("Loading test cases...")
        test_loader = unittest.TestLoader()
        dir = os.path.dirname(__file__)
        self.test_suite = test_loader.discover(dir, pattern='test_*.py')
        for test in self.test_suite:
            if isinstance(test, unittest.TestSuite):
                for case in test:
                    if isinstance(case, unittest.TestSuite):
                        for subtest in case:
                            if isinstance(subtest, unittest.TestCase):
                                item = QListWidgetItem(subtest.id())
                                item.setCheckState(Qt.CheckState.Unchecked)
                                self.test_list.addItem(item)
                    elif isinstance(case, unittest.TestCase):
                        item = QListWidgetItem(case.id())
                        item.setCheckState(Qt.CheckState.Unchecked)
                        self.test_list.addItem(item)
            elif isinstance(test, unittest.TestCase):
                item = QListWidgetItem(test.id())
                item.setCheckState(Qt.CheckState.Unchecked)
                self.test_list.addItem(item)
        self.log("Test cases loaded.")

    def run_tests(self):
        """
        Run the selected tests and display results in the UI.
        """
        self.log("Running selected tests...")
        selected_tests = []
        for index in range(self.test_list.count()):
            item = self.test_list.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                selected_tests.append(item.text())

        if not selected_tests:
            self.log("No tests selected.")
            return

        # Create a Test Suite with selected tests
        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for test_name in selected_tests:
            try:
                suite.addTest(test_loader.loadTestsFromName(test_name))
            except Exception as e:
                self.log(f"Error loading test '{test_name}': {e}")

        # Run the tests
        runner = unittest.TextTestRunner(resultclass=CustomTestResult, verbosity=2)
        result = runner.run(suite)

        # Display results
        total_tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        passed = total_tests - (failures + errors)
        self.progress_bar.setMaximum(total_tests)
        self.progress_bar.setValue(passed)
        self.log(f"Total Tests: {total_tests}, Passed: {passed}, Failures: {failures}, Errors: {errors}")

        # Highlight failures/errors in the test list
        for failure in result.failures + result.errors:
            for index in range(self.test_list.count()):
                item = self.test_list.item(index)
                if item.text() == failure[0].id():
                    item.setBackground(QColor("#FFCCCC"))
                    item.setIcon(QIcon.fromTheme("dialog-error"))

    def log(self, message):
        """
        Logs a message to the log viewer.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_viewer.append(f"[{timestamp}] {message}")
        self.log_viewer.ensureCursorVisible()

class CustomTestResult(unittest.TextTestResult):
    """
    Custom Test Result class to handle detailed test result logging.
    """
    def addSuccess(self, test):
        super().addSuccess(test)
        logging.info(f"Test Passed: {test.id()}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        logging.error(f"Test Failed: {test.id()}\n{self._exc_info_to_string(err, test)}")

    def addError(self, test, err):
        super().addError(test, err)
        logging.error(f"Test Error: {test.id()}\n{self._exc_info_to_string(err, test)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestRunnerInterface()
    window.show()
    sys.exit(app.exec())

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo QT6 Test Runner Interface
# -----------------------------------------------------------------------------------------------------
