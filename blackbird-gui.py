import sys
import subprocess
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, 
                             QCheckBox, QGroupBox, QFormLayout, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class BlackbirdWorker(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        for line in self.process.stdout:
            self.output_signal.emit(line.strip())
        self.process.wait()

    def terminate(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

class BlackbirdGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackbird OSINT Tool")
        self.setGeometry(100, 100, 800, 800)
        self.worker = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Input Group
        input_group = QGroupBox("Input")
        input_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        input_layout.addRow("Username(s) (comma-separated):", self.username_input)
        
        self.email_input = QLineEdit()
        input_layout.addRow("Email(s) (comma-separated):", self.email_input)
        
        self.file_input = QLineEdit()
        file_button = QPushButton("Select File")
        file_button.clicked.connect(self.select_file)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(file_button)
        input_layout.addRow("File:", file_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Options Group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        self.permute_checkbox = QCheckBox("Permute username (works with single username only)")
        options_layout.addWidget(self.permute_checkbox)
        
        self.permuteall_checkbox = QCheckBox("Permute all elements (works with single username only)")
        options_layout.addWidget(self.permuteall_checkbox)
        
        self.no_nsfw_checkbox = QCheckBox("Exclude NSFW sites")
        options_layout.addWidget(self.no_nsfw_checkbox)
        
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(QLabel("Proxy:"))
        self.proxy_input = QLineEdit()
        proxy_layout.addWidget(self.proxy_input)
        options_layout.addLayout(proxy_layout)
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Timeout (seconds):"))
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(1, 300)
        self.timeout_spinbox.setValue(30)
        timeout_layout.addWidget(self.timeout_spinbox)
        options_layout.addLayout(timeout_layout)
        
        self.no_update_checkbox = QCheckBox("Don't check for updates")
        options_layout.addWidget(self.no_update_checkbox)
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter:"))
        self.filter_input = QLineEdit()
        filter_layout.addWidget(self.filter_input)
        options_layout.addLayout(filter_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Output Options
        output_group = QGroupBox("Output Options")
        output_layout = QHBoxLayout()
        self.csv_checkbox = QCheckBox("CSV (Results)")
        self.pdf_checkbox = QCheckBox("PDF (Results)")
        self.verbose_checkbox = QCheckBox("Verbose (LOGS)")
        self.dump_checkbox = QCheckBox("Dump HTML (Results)")
        output_layout.addWidget(self.csv_checkbox)
        output_layout.addWidget(self.pdf_checkbox)
        output_layout.addWidget(self.verbose_checkbox)
        output_layout.addWidget(self.dump_checkbox)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Instagram Session ID
        instagram_group = QGroupBox("Instagram Enhanced Metadata")
        instagram_layout = QHBoxLayout()
        self.instagram_session_id = QLineEdit()
        instagram_layout.addWidget(QLabel("Instagram Session ID:"))
        instagram_layout.addWidget(self.instagram_session_id)
        instagram_help_button = QPushButton("?")
        instagram_help_button.clicked.connect(self.show_instagram_help)
        instagram_layout.addWidget(instagram_help_button)
        instagram_group.setLayout(instagram_layout)
        layout.addWidget(instagram_group)

        # Run and Stop buttons
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Blackbird")
        self.run_button.clicked.connect(self.run_blackbird)
        button_layout.addWidget(self.run_button)
        
        self.stop_button = QPushButton("Stop Blackbird")
        self.stop_button.clicked.connect(self.stop_blackbird)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.file_input.setText(file_name)

    def show_instagram_help(self):
        QMessageBox.information(self, "Instagram Session ID Help",
                                "To use enhanced Instagram metadata extraction:\n\n"
                                "1. Log in to Instagram in your browser\n"
                                "2. Open developer tools (F12)\n"
                                "3. Go to Application > Cookies\n"
                                "4. Find the 'sessionid' cookie\n"
                                "5. Copy its value and paste it here")

    def run_blackbird(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()

        command = ["python", "blackbird.py"]
        
        if self.username_input.text():
            usernames = [u.strip() for u in self.username_input.text().split(',')]
            for username in usernames:
                command.extend(["-u", username])
            
            if len(usernames) == 1:
                if self.permute_checkbox.isChecked():
                    command.append("--permute")
                elif self.permuteall_checkbox.isChecked():
                    command.append("--permuteall")
        
        if self.email_input.text():
            emails = [e.strip() for e in self.email_input.text().split(',')]
            for email in emails:
                command.extend(["-e", email])
        
        if self.file_input.text():
            if self.username_input.text():
                command.extend(["--username-file", self.file_input.text()])
            elif self.email_input.text():
                command.extend(["--email-file", self.file_input.text()])
        
        if self.no_nsfw_checkbox.isChecked():
            command.append("--no-nsfw")
        
        if self.proxy_input.text():
            command.extend(["--proxy", self.proxy_input.text()])
        
        command.extend(["--timeout", str(self.timeout_spinbox.value())])
        
        if self.no_update_checkbox.isChecked():
            command.append("--no-update")
        
        if self.filter_input.text():
            command.extend(["--filter", self.filter_input.text()])
        
        if self.csv_checkbox.isChecked():
            command.append("--csv")
        
        if self.pdf_checkbox.isChecked():
            command.append("--pdf")
        
        if self.verbose_checkbox.isChecked():
            command.append("--verbose")
        
        if self.dump_checkbox.isChecked():
            command.append("--dump")

        if self.instagram_session_id.text():
            os.environ["INSTAGRAM_SESSION_ID"] = self.instagram_session_id.text()

        self.output_area.clear()
        self.worker = BlackbirdWorker(" ".join(command))
        self.worker.output_signal.connect(self.update_output)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_blackbird(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_output(self, text):
        scrollbar = self.output_area.verticalScrollBar()
        was_at_bottom = scrollbar.value() == scrollbar.maximum()

        self.output_area.append(text)

        if was_at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    def on_worker_finished(self):
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackbirdGUI()
    window.show()
    sys.exit(app.exec())
