#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from random import randint
import sys
import logging
import asyncio
from core.contribution_generator import ContributionGenerator
from core.contribution_analyzer import ContributionAnalyzer

from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------------------------------------------------------------------------------
# @ Main Git Contribution Analyzer and Generator with QT6 GUI
# -----------------------------------------------------------------------------------------------------

class ContributionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Git Contribution Analyzer and Generator")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # UI Elements
        self.repo_path_input = QLineEdit(self)
        self.repo_path_input.setPlaceholderText("Select or enter repository path")
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_repo_path)

        self.days_before_input = QLineEdit(self)
        self.days_before_input.setPlaceholderText("Days Before (e.g., 30)")
        self.days_after_input = QLineEdit(self)
        self.days_after_input.setPlaceholderText("Days After (e.g., 10)")
        self.frequency_input = QLineEdit(self)
        self.frequency_input.setPlaceholderText("Frequency (e.g., 80)")
        self.max_commits_input = QLineEdit(self)
        self.max_commits_input.setPlaceholderText("Max Commits Per Day (e.g., 10)")
        self.repository_url_input = QLineEdit(self)
        self.repository_url_input.setPlaceholderText("Repository URL for Analysis (optional)")

        self.run_button = QPushButton("Run Contribution Generator and Analyzer", self)
        self.run_button.clicked.connect(self.run_contribution_process)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)

        # Add widgets to layout
        self.layout.addWidget(QLabel("Repository Path:"))
        self.layout.addWidget(self.repo_path_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(QLabel("Days Before:"))
        self.layout.addWidget(self.days_before_input)
        self.layout.addWidget(QLabel("Days After:"))
        self.layout.addWidget(self.days_after_input)
        self.layout.addWidget(QLabel("Frequency (Percentage of Days with Commits):"))
        self.layout.addWidget(self.frequency_input)
        self.layout.addWidget(QLabel("Max Commits Per Day:"))
        self.layout.addWidget(self.max_commits_input)
        self.layout.addWidget(QLabel("Repository URL for Analysis (Optional):"))
        self.layout.addWidget(self.repository_url_input)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(QLabel("Log Output:"))
        self.layout.addWidget(self.log_output)

    def browse_repo_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Repository Directory")
        if directory:
            self.repo_path_input.setText(directory)

    def run_contribution_process(self):
        repo_path = self.repo_path_input.text()
        days_before = int(self.days_before_input.text()) if self.days_before_input.text() else 0
        days_after = int(self.days_after_input.text()) if self.days_after_input.text() else 0
        frequency = int(self.frequency_input.text()) if self.frequency_input.text() else 80
        max_commits = int(self.max_commits_input.text()) if self.max_commits_input.text() else 10
        repository_url = self.repository_url_input.text() if self.repository_url_input.text() else None

        self.progress_bar.setValue(0)
        self.log_output.append("Starting contribution generation and analysis...")

        # Run the generator and analyzer in a separate thread
        self.worker = ContributionWorker(repo_path, days_before, days_after, frequency, max_commits, repository_url)
        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.update_log)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_log(self, message):
        self.log_output.append(message)

class ContributionWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)

    def __init__(self, repo_path, days_before, days_after, frequency, max_commits, repository_url):
        super().__init__()
        self.repo_path = repo_path
        self.days_before = days_before
        self.days_after = days_after
        self.frequency = frequency / 100.0
        self.max_commits = max_commits
        self.repository_url = repository_url

    def run(self):
        try:
            curr_date = datetime.now()
            contribution_generator = ContributionGenerator(repo_path=self.repo_path)

            start_date = curr_date - timedelta(days=self.days_before)
            end_date = curr_date + timedelta(days=self.days_after)

            self.log.emit(f"Generating contributions from {start_date} to {end_date}...")
            contribution_generator.generate_contributions_over_period(
                days=(self.days_before + self.days_after), max_commits_per_day=self.max_commits
            )
            self.progress.emit(50)
            self.log.emit("Contributions generated successfully.")

            if self.repository_url:
                self.log.emit(f"Analyzing repository contributions for {self.repository_url}...")
                analyzer = ContributionAnalyzer(self.repository_url)
                contributions = asyncio.run(analyzer.analyze_contributions(start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')))
                self.log.emit(f"Total contributions: {contributions}")
                top_contributors = asyncio.run(analyzer.get_top_contributors(start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')))
                self.log.emit(f"Top contributors: {top_contributors}")

            self.progress.emit(100)
            self.log.emit("Process completed successfully.")
        except Exception as e:
            self.log.emit(f"Error: {e}")
            self.progress.emit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ContributionApp()
    main_window.show()
    sys.exit(app.exec())

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Main Git Contribution Analyzer and Generator with QT6 GUI
# -----------------------------------------------------------------------------------------------------
