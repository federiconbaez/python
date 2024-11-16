from datetime import datetime, timedelta
import os
import sys
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
from pathlib import Path
import re
from git import Repo, GitCommandError
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QLabel, QTreeWidget, QTreeWidgetItem, QProgressBar, 
    QDateTimeEdit, QSpinBox, QHBoxLayout, QMessageBox,
    QDialog, QTextEdit, QScrollArea, QFrame
)
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QFont, QColor

@dataclass
class FileInfo:
    """Dataclass to store file information with enhanced metadata"""
    path: str
    size: int
    last_modified: datetime
    content: str = ""
    type: str = ""  # Component, Hook, Context, etc.
    category: str = ""  # UI, Logic, Data, etc.
    complexity: int = 0  # Calculated based on content analysis

class CommitMessageGenerator:
    """Intelligent commit message generator based on file context"""
    
    # Commit message templates by file type
    COMPONENT_MESSAGES = [
        "feat({component}): implement new {type} component",
        "update({component}): enhance {type} component functionality",
        "style({component}): improve {type} component styling",
        "refactor({component}): optimize {type} component structure",
        "fix({component}): resolve issues in {type} component",
    ]
    
    HOOK_MESSAGES = [
        "feat(hooks): add new {name} hook for {purpose}",
        "refactor(hooks): optimize {name} hook implementation",
        "update(hooks): enhance {name} hook functionality",
        "fix(hooks): resolve edge cases in {name} hook",
    ]
    
    CONTEXT_MESSAGES = [
        "feat(context): implement {name} context provider",
        "update(context): enhance {name} context functionality",
        "refactor(context): optimize {name} context structure",
    ]
    
    STYLE_MESSAGES = [
        "style: update {component} styling",
        "style: enhance visual appearance of {component}",
        "style: implement responsive design for {component}",
        "style: add new theme variations for {component}",
    ]
    
    UTILITY_MESSAGES = [
        "feat(utils): add new {name} utility function",
        "update(utils): enhance {name} utility functionality",
        "refactor(utils): optimize {name} utility implementation",
    ]
    
    @classmethod
    def analyze_file_type(cls, file_path: str, content: str) -> Tuple[str, str, int]:
        """
        Analyze file content to determine type, category and complexity
        """
        file_name = Path(file_path).stem
        ext = Path(file_path).suffix
        
        # Determine file type
        if re.search(r'function\s+use[A-Z]', content):
            type = "Hook"
            category = "Logic"
        elif re.search(r'React\.createContext|createContext', content):
            type = "Context"
            category = "Data"
        elif re.search(r'export\s+default\s+function|class\s+\w+\s+extends\s+React', content):
            type = "Component"
            category = "UI" if re.search(r'className|style=|css|scss', content) else "Logic"
        elif ext in ['.css', '.scss', '.sass']:
            type = "Style"
            category = "UI"
        else:
            type = "Utility"
            category = "Logic"
            
        # Calculate complexity
        complexity = len(re.findall(r'function|class|if|for|while|switch|try', content))
        
        return type, category, complexity

    @classmethod
    def generate_message(cls, files: List[FileInfo]) -> str:
        """
        Generate intelligent commit message based on files being committed
        """
        if not files:
            return "chore: routine update"
            
        # Group files by type
        file_groups = {}
        for file in files:
            file_groups.setdefault(file.type, []).append(file)
            
        # Generate message based on predominant type
        main_type = max(file_groups.keys(), key=lambda k: len(file_groups[k]))
        files_of_main_type = file_groups[main_type]
        
        if main_type == "Component":
            template = random.choice(cls.COMPONENT_MESSAGES)
            component = Path(files_of_main_type[0].path).stem
            return template.format(
                component=component,
                type=files_of_main_type[0].category.lower()
            )
        elif main_type == "Hook":
            template = random.choice(cls.HOOK_MESSAGES)
            hook_name = Path(files_of_main_type[0].path).stem
            purpose = "state management" if "State" in hook_name else "data fetching"
            return template.format(name=hook_name, purpose=purpose)
        elif main_type == "Context":
            template = random.choice(cls.CONTEXT_MESSAGES)
            context_name = Path(files_of_main_type[0].path).stem
            return template.format(name=context_name)
        elif main_type == "Style":
            template = random.choice(cls.STYLE_MESSAGES)
            component = Path(files_of_main_type[0].path).stem
            return template.format(component=component)
        else:
            template = random.choice(cls.UTILITY_MESSAGES)
            util_name = Path(files_of_main_type[0].path).stem
            return template.format(name=util_name)

class ProjectScanWorker(QThread):
    """Worker thread for project scanning"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(list)
    
    def __init__(self, scanner: 'ReactProjectScanner'):
        super().__init__()
        self.scanner = scanner
        
    def run(self):
        try:
            files = self.scanner.scan_project(self.progress.emit)
            self.finished.emit(files)
        except Exception as e:
            logging.error(f"Scan error: {str(e)}")
            self.finished.emit([])

class CommitPreviewDialog(QDialog):
    """Dialog for previewing commits before execution"""
    
    def __init__(self, commits: List[Tuple[datetime, List[FileInfo]]], parent=None):
        super().__init__(parent)
        self.commits = commits
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Commit Preview")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Preview area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        for date, files in self.commits:
            # Create commit group frame
            commit_frame = QFrame()
            commit_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
            commit_layout = QVBoxLayout(commit_frame)
            
            # Commit header
            message = CommitMessageGenerator.generate_message(files)
            header = QLabel(f"<b>{date.strftime('%Y-%m-%d %H:%M:%S')}</b><br>{message}")
            header.setStyleSheet("color: #2d5986;")
            commit_layout.addWidget(header)
            
            # Files list
            files_widget = QTreeWidget()
            files_widget.setHeaderLabels(["File", "Type", "Category", "Complexity"])
            files_widget.setAlternatingRowColors(True)
            
            for file in files:
                item = QTreeWidgetItem([
                    file.path,
                    file.type,
                    file.category,
                    str(file.complexity)
                ])
                files_widget.addTopLevelItem(item)
            
            commit_layout.addWidget(files_widget)
            content_layout.addWidget(commit_frame)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Proceed with Commits")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

class ReactProjectScanner:
    """Enhanced scanner with intelligent commit messages and UI"""
    
    def __init__(
        self,
        project_path: str,
        start_date: datetime,
        end_date: datetime,
        commits_per_day: int = 10,
        ignore_patterns: List[str] = None
    ):
        self.project_path = Path(project_path)
        self.start_date = start_date
        self.end_date = end_date
        self.commits_per_day = commits_per_day
        self.ignore_patterns = ignore_patterns or [
            'node_modules', 'build', 'dist', '.git',
            '__pycache__', '.env', '.DS_Store'
        ]
        
        self.files: List[FileInfo] = []
        self.date_groups: Dict[datetime, List[FileInfo]] = {}
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('react_scanner.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def scan_project(self, progress_callback: Optional[callable] = None) -> List[FileInfo]:
        """
        Scan the React project directory with enhanced file analysis
        """
        self.logger.info(f"Starting project scan at {self.project_path}")
        self.files = []
        
        try:
            total_files = sum([len(files) for _, _, files in os.walk(self.project_path)])
            processed = 0
            
            for root, dirs, files in os.walk(self.project_path):
                dirs[:] = [d for d in dirs if not any(
                    ignore in d for ignore in self.ignore_patterns
                )]
                
                for file in files:
                    if self._is_valid_file(file):
                        file_path = Path(root) / file
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Enhanced file analysis
                            file_type, category, complexity = CommitMessageGenerator.analyze_file_type(
                                str(file_path),
                                content
                            )
                            
                            file_info = FileInfo(
                                path=str(file_path.relative_to(self.project_path)),
                                size=os.path.getsize(file_path),
                                last_modified=datetime.fromtimestamp(
                                    os.path.getmtime(file_path)
                                ),
                                content=content,
                                type=file_type,
                                category=category,
                                complexity=complexity
                            )
                            self.files.append(file_info)
                            
                        except Exception as e:
                            self.logger.error(f"Error processing file {file_path}: {str(e)}")
                    
                    processed += 1
                    if progress_callback:
                        progress = int((processed / total_files) * 100)
                        progress_callback(progress, f"Processing: {file}")
            
            self.logger.info(f"Scan completed. Found {len(self.files)} files")
            return self.files
            
        except Exception as e:
            self.logger.error(f"Error scanning project: {str(e)}")
            raise

    def prepare_commits(self) -> List[Tuple[datetime, List[FileInfo]]]:
        """
        Prepare commits with intelligent distribution and grouping
        """
        if not self.files:
            raise ValueError("No files to commit. Run scan_project() first.")
            
        commits = []
        total_days = (self.end_date - self.start_date).days
        
        # Group files by type and category
        type_groups = {}
        for file in self.files:
            key = (file.type, file.category)
            type_groups.setdefault(key, []).append(file)
        
        # Distribute files across dates while keeping related files together
        current_date = self.start_date
        while current_date <= self.end_date:
            # Randomize number of commits for the day
            daily_commits = random.randint(1, self.commits_per_day)
            
            for _ in range(daily_commits):
                if not any(type_groups.values()):
                    break
                
                # Select a random group that still has files
                available_groups = [(k, v) for k, v in type_groups.items() if v]
                if not available_groups:
                    break
                    
                group_key, group_files = random.choice(available_groups)
                
                # Take a random number of files from the group
                files_count = random.randint(1, min(5, len(group_files)))
                commit_files = group_files[:files_count]
                type_groups[group_key] = group_files[files_count:]
                
                # Generate commit time during working hours
                hour = random.randint(9, 18)
                minute = random.randint(0, 59)
                commit_time = current_date.replace(hour=hour, minute=minute)
                
                commits.append((commit_time, commit_files))
            
            current_date += timedelta(days=1)
        
        return commits

    def show_preview(self, parent: Optional[QWidget] = None) -> bool:
        """
        Show commit preview dialog
        
        Returns:
            bool: True if user accepted, False if cancelled
        """
        commits = self.prepare_commits()
        dialog = CommitPreviewDialog(commits, parent)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            self._execute_commits(commits)
            return True
        return False

    def _execute_commits(self, commits: List[Tuple[datetime, List[FileInfo]]]) -> None:
        """Execute the prepared commits"""
        try:
            repo = Repo(self.project_path)
        except:
            repo = Repo.init(self.project_path)
            
        for commit_date, files in commits:
            try:
                # Stage files
                for file in files:
                    file_path = Path(self.project_path) / file.path
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file.content)
                    
                    repo.index.add([str(file.path)])
                
                # Create commit with intelligent message
                message = CommitMessageGenerator.generate_message(files)
                repo.index.commit(
                    message,
                    author_date=commit_date.isoformat(),
                    commit_date=commit_date.isoformat()
                )
                
                self.logger.info(
                    f"Created commit at {commit_date} with message: {message}"
                )
                
            except GitCommandError as e:
                self.logger.error(f"Git error during commit: {str(e)}")
            except Exception as e:
                self.logger.error(f"Error creating commit: {str(e)}")

    def _is_valid_file(self, filename: str) -> bool:
        """Check if a file should be included in the scan"""
        # React project specific extensions
        valid_extensions = {
            '.js', '.jsx', '.ts', '.tsx', '.css', '.scss',
            '.json', '.md', '.html', '.svg', '.mjs', '.cjs'
        }
        
        return (
            Path(filename).suffix in valid_extensions and
            not any(ignore in filename for ignore in self.ignore_patterns)
        )

class ReactProjectScannerUI(QMainWindow):
    """Main UI for the React Project Scanner"""
    
    def __init__(self):
        super().__init__()
        self.scanner = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("React Project Scanner")
        self.setMinimumSize(1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Project selection
        project_layout = QHBoxLayout()
        self.project_label = QLabel("Project Path:")
        self.project_path = QLabel("No project selected")
        self.select_project_btn = QPushButton("Select Project")
        self.select_project_btn.clicked.connect(self.select_project)
        
        project_layout.addWidget(self.project_label)
        project_layout.addWidget(self.project_path, stretch=1)
        project_layout.addWidget(self.select_project_btn)
        layout.addLayout(project_layout)
        
        # Date range selection
        date_layout = QHBoxLayout()
        
        # Start date
        start_date_widget = QWidget()
        start_date_layout = QVBoxLayout(start_date_widget)
        self.start_date_label = QLabel("Start Date:")
        self.start_date_edit = QDateTimeEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDateTime(
            QDateTime.currentDateTime().addYears(-1)
        )
        start_date_layout.addWidget(self.start_date_label)
        start_date_layout.addWidget(self.start_date_edit)
        
        # End date
        end_date_widget = QWidget()
        end_date_layout = QVBoxLayout(end_date_widget)
        self.end_date_label = QLabel("End Date:")
        self.end_date_edit = QDateTimeEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDateTime(QDateTime.currentDateTime())
        end_date_layout.addWidget(self.end_date_label)
        end_date_layout.addWidget(self.end_date_edit)
        
        # Commits per day
        commits_widget = QWidget()
        commits_layout = QVBoxLayout(commits_widget)
        self.commits_label = QLabel("Max Commits per Day:")
        self.commits_spin = QSpinBox()
        self.commits_spin.setRange(1, 50)
        self.commits_spin.setValue(10)
        commits_layout.addWidget(self.commits_label)
        commits_layout.addWidget(self.commits_spin)
        
        date_layout.addWidget(start_date_widget)
        date_layout.addWidget(end_date_widget)
        date_layout.addWidget(commits_widget)
        layout.addLayout(date_layout)
        
        # File tree
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels([
            "File", "Type", "Category", "Size (KB)", "Modified", "Complexity"
        ])
        self.file_tree.setAlternatingRowColors(True)
        layout.addWidget(self.file_tree)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.scan_button = QPushButton("Scan Project")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setEnabled(False)
        
        self.preview_button = QPushButton("Preview Commits")
        self.preview_button.clicked.connect(self.preview_commits)
        self.preview_button.setEnabled(False)
        
        button_layout.addWidget(self.scan_button)
        button_layout.addWidget(self.preview_button)
        layout.addLayout(button_layout)

    def select_project(self):
        """Handle project selection"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select React Project Directory",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if directory:
            self.project_path.setText(directory)
            self.scan_button.setEnabled(True)
            self.scanner = ReactProjectScanner(
                project_path=directory,
                start_date=self.start_date_edit.dateTime().toPython(),
                end_date=self.end_date_edit.dateTime().toPython(),
                commits_per_day=self.commits_spin.value()
            )

    def start_scan(self):
        """Start project scanning"""
        if not self.scanner:
            return
            
        self.progress_bar.setVisible(True)
        self.scan_button.setEnabled(False)
        self.preview_button.setEnabled(False)
        self.file_tree.clear()
        
        # Create and start worker thread
        self.scan_worker = ProjectScanWorker(self.scanner)
        self.scan_worker.progress.connect(self.update_progress)
        self.scan_worker.finished.connect(self.scan_completed)
        self.scan_worker.start()

    def update_progress(self, value: int, message: str):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)

    def scan_completed(self, files: List[FileInfo]):
        """Handle scan completion"""
        self.progress_bar.setVisible(False)
        self.preview_button.setEnabled(True)
        self.scan_button.setEnabled(True)
        
        # Update file tree
        self.file_tree.clear()
        for file in files:
            item = QTreeWidgetItem([
                file.path,
                file.type,
                file.category,
                f"{file.size / 1024:.2f}",
                file.last_modified.strftime("%Y-%m-%d %H:%M"),
                str(file.complexity)
            ])
            
            # Color coding based on type
            colors = {
                "Component": QColor("#e6f3ff"),
                "Hook": QColor("#fff0e6"),
                "Context": QColor("#e6ffe6"),
                "Style": QColor("#ffe6e6"),
                "Utility": QColor("#f2e6ff")
            }
            
            for col in range(item.columnCount()):
                item.setBackground(col, colors.get(file.type, QColor("white")))
            
            self.file_tree.addTopLevelItem(item)
        
        self.file_tree.resizeColumnToContents(0)
        self.status_label.setText(f"Scan completed: {len(files)} files found")

    def preview_commits(self):
        """Show commit preview dialog"""
        if not self.scanner:
            return
            
        try:
            if self.scanner.show_preview(self):
                QMessageBox.information(
                    self,
                    "Success",
                    "Commits created successfully!"
                )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error creating commits: {str(e)}"
            )

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Modern look
    
    # Set stylesheet for better appearance
    app.setStyleSheet("""
        QMainWindow {
            background: #f5f5f5;
        }
        QPushButton {
            padding: 5px 15px;
            border-radius: 3px;
            background: #2196F3;
            color: white;
            min-width: 80px;
        }
        QPushButton:disabled {
            background: #B0BEC5;
        }
        QTreeWidget {
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        QLabel {
            color: #333;
        }
        QProgressBar {
            border: 1px solid #ddd;
            border-radius: 3px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #2196F3;
        }
    """)
    
    window = ReactProjectScannerUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()