import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, 
                             QCheckBox, QGroupBox, QFormLayout, QSpinBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class BlackbirdWorker(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        for line in process.stdout:
            self.output_signal.emit(line.strip())
        process.wait()

class BlackbirdGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackbird OSINT Tool")
        self.setGeometry(100, 100, 800, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Input Group
        input_group = QGroupBox("Input")
        input_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        input_layout.addRow("Username:", self.username_input)
        
        self.email_input = QLineEdit()
        input_layout.addRow("Email:", self.email_input)
        
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
        
        self.permute_checkbox = QCheckBox("Permute usernames")
        options_layout.addWidget(self.permute_checkbox)
        
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
        self.csv_checkbox = QCheckBox("CSV")
        self.pdf_checkbox = QCheckBox("PDF")
        self.verbose_checkbox = QCheckBox("Verbose")
        output_layout.addWidget(self.csv_checkbox)
        output_layout.addWidget(self.pdf_checkbox)
        output_layout.addWidget(self.verbose_checkbox)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Run button
        run_button = QPushButton("Run Blackbird")
        run_button.clicked.connect(self.run_blackbird)
        layout.addWidget(run_button)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.file_input.setText(file_name)

    def run_blackbird(self):
        command = ["python", "blackbird.py"]
        
        if self.username_input.text():
            command.extend(["-u", self.username_input.text()])
        
        if self.email_input.text():
            command.extend(["-e", self.email_input.text()])
        
        if self.file_input.text():
            if self.username_input.text():
                command.extend(["--username-file", self.file_input.text()])
            elif self.email_input.text():
                command.extend(["--email-file", self.file_input.text()])
        
        if self.permute_checkbox.isChecked():
            command.append("--permute")
        
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

        self.output_area.clear()
        self.worker = BlackbirdWorker(" ".join(command))
        self.worker.output_signal.connect(self.update_output)
        self.worker.start()

    def update_output(self, text):
        self.output_area.append(text)
        self.output_area.verticalScrollBar().setValue(self.output_area.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackbirdGUI()
    window.show()
    sys.exit(app.exec())
