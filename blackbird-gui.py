import sys
import subprocess
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, 
                             QCheckBox, QGroupBox, QFormLayout, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Worker class that handles executing the Blackbird command in a separate thread
class BlackbirdWorker(QThread):
    # Signal to send output to the main thread
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        # Initialize with the command to run
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        # Run the command using subprocess and capture output
        self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        for line in self.process.stdout:
            # Emit output line by line to update the UI
            self.output_signal.emit(line.strip())
        self.process.wait()

    def terminate(self):
        # Terminate the process if it's running
        if self.process:
            self.process.terminate()
            self.process.wait()

# Main GUI class for the Blackbird OSINT tool
class BlackbirdGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.setWindowTitle("Blackbird OSINT Tool")
        self.setGeometry(100, 100, 1000, 800)
        self.worker = None

        # Create the central widget and layout for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Input Group: For entering usernames, emails, and file selection
        input_group = QGroupBox("Input")
        input_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        input_layout.addRow("Username(s):", self.username_input)
        
        self.email_input = QLineEdit()
        input_layout.addRow("Email(s):", self.email_input)
        
        # self.file_input = QLineEdit()
        # file_button = QPushButton("Select File")
        # file_button.clicked.connect(self.select_file)  # Open file dialog on click
        # file_layout = QHBoxLayout()
        # file_layout.addWidget(self.file_input)
        # file_layout.addWidget(file_button)
        # input_layout.addRow("File:", file_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Options Group: Various checkboxes for additional configuration
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        # Permute username checkbox with help button
        self.permute_checkbox = QCheckBox("Permute username")
        options_layout.addWidget(self.permute_checkbox)

        permute_help_button = QPushButton("?")
        permute_help_button.setFixedSize(30, 30)  # Set a fixed size for the button (width, height)
        permute_help_button.clicked.connect(self.show_permute_help)  # Connect to the help function
        options_layout.addWidget(permute_help_button)

        # Permute all elements checkbox with help button
        self.permuteall_checkbox = QCheckBox("Permute all")
        options_layout.addWidget(self.permuteall_checkbox)

        permuteall_help_button = QPushButton("?")
        permuteall_help_button.setFixedSize(30, 30)  # Set a fixed size for the button (width, height)
        permuteall_help_button.clicked.connect(self.show_permuteall_help)  # Connect to the help function
        options_layout.addWidget(permuteall_help_button)

        
        self.no_nsfw_checkbox = QCheckBox("Exclude NSFW sites")
        options_layout.addWidget(self.no_nsfw_checkbox)
        
        # Proxy input
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(QLabel("Proxy:"))
        self.proxy_input = QLineEdit()
        proxy_layout.addWidget(self.proxy_input)
        options_layout.addLayout(proxy_layout)
        
        # Timeout input with spinner for seconds
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Timeout (seconds):"))
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(1, 300)  # Limit timeout to 1-300 seconds
        self.timeout_spinbox.setValue(30)  # Default timeout is 30 seconds
        timeout_layout.addWidget(self.timeout_spinbox)
        options_layout.addLayout(timeout_layout)
        
        # Checkbox to disable update checks
        self.no_update_checkbox = QCheckBox("Don't check for updates")
        options_layout.addWidget(self.no_update_checkbox)
        
        # Filter input field with a help button
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter:"))
        self.filter_input = QLineEdit()
        filter_layout.addWidget(self.filter_input)

        # Create a help button and connect it to the help function
        filter_help_button = QPushButton("?")
        filter_help_button.clicked.connect(self.show_filter_help)  # Connect the button to the help function
        filter_layout.addWidget(filter_help_button)

        options_layout.addLayout(filter_layout)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)


        # Output Options Group: Allows user to specify output types
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

        # Instagram session ID input for enhanced metadata extraction
        instagram_group = QGroupBox("Instagram Enhanced Metadata")
        instagram_layout = QHBoxLayout()
        self.instagram_session_id = QLineEdit()
        instagram_layout.addWidget(QLabel("Instagram Session ID:"))
        instagram_layout.addWidget(self.instagram_session_id)
        instagram_help_button = QPushButton("?")
        instagram_help_button.clicked.connect(self.show_instagram_help)  # Show help on click
        instagram_layout.addWidget(instagram_help_button)
        instagram_group.setLayout(instagram_layout)
        layout.addWidget(instagram_group)

        # Run and Stop buttons
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Blackbird")
        self.run_button.clicked.connect(self.run_blackbird)  # Start Blackbird on click
        button_layout.addWidget(self.run_button)
        
        self.stop_button = QPushButton("Stop Blackbird")
        self.stop_button.clicked.connect(self.stop_blackbird)  # Stop Blackbird on click
        self.stop_button.setEnabled(False)  # Disable initially
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)

        # Output area for displaying logs and results
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

    # def select_file(self):
    #     # Open a file dialog to select a file and set its path in the input field
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
    #     if file_name:
    #         self.file_input.setText(file_name)

    def show_instagram_help(self):
        # Display instructions for obtaining the Instagram session ID
        QMessageBox.information(self, "Instagram Session ID Help",
                                "To use enhanced Instagram metadata extraction:\n\n"
                                "1. Log in to Instagram in your browser\n"
                                "2. Open developer tools (F12)\n"
                                "3. Go to Application > Cookies\n"
                                "4. Find the 'sessionid' cookie\n"
                                "5. Copy its value and paste it here")

    def show_filter_help(self):
        # Display a message box with the detailed help for the filter
        QMessageBox.information(self, "Filter Help",
                                "The 'Filter' option allows you to create custom search filters using specific properties and operators.\n\n"
                                "Properties:\n"
                                "- name: Name of the site being checked\n"
                                "- cat: Category of the site\n"
                                "- uri_check: The URL used to check for the existence of an account\n"
                                "- e_code: Expected HTTP status code when an account exists\n"
                                "- e_string: A string expected in the response when an account exists\n"
                                "- m_string: A string expected in the response when an account does not exist\n"
                                "- m_code: Expected HTTP status code when an account does not exist\n\n"
                                "Operators:\n"
                                "- =: Equal to\n"
                                "- ~: Contains\n"
                                "- >: Greater than\n"
                                "- <: Less than\n"
                                "- >=: Greater than or equal to\n"
                                "- <=: Less than or equal to\n"
                                "- !=: Not equal to\n\n"
                                "Examples:\n"
                                "1. Filter by Name Contains 'Mastodon':\n"
                                "   python blackbird.py --filter \"name~Mastodon\" --username crash\n\n"
                                "2. Filter by Existent Code Greater Than 200:\n"
                                "   python blackbird.py --filter \"e_code>200\" --username crash\n\n"
                                "3. Filter by Category Equals 'social' and URI Contains '101010':\n"
                                "   python blackbird.py --filter \"cat=social and uri_check~101010\" --username crash\n\n"
                                "4. Filter by Error String Equals '@101010.pl' or Inexistent Code Less Than or Equal to 404:\n"
                                "   python blackbird.py --filter \"e_string=@101010.pl or m_code<=404\" --username crash")


    def show_permute_help(self):
        # Display a message box with details about permuting usernames
        QMessageBox.information(self, "Permute Username Help",
                                "The '--permute' option generates variations of a given username.\n\n"
                                "For example, if your username is 'balestek86', the permutations would be:\n"
                                "balestek86\n"
                                "_balestek86\n"
                                "balestek86_\n"
                                "balestek_86\n"
                                "balestek-86\n"
                                "balestek.86\n"
                                "86balestek\n"
                                "_86balestek\n"
                                "86balestek_\n"
                                "86_balestek\n"
                                "86-balestek\n"
                                "86.balestek\n\n"
                                "You can use '--permute' to create these variations and search them.")

    def show_permuteall_help(self):
        # Display a message box with details about permuting all elements
        QMessageBox.information(self, "Permute All Elements Help",
                                "The '--permuteall' option generates a broader set of permutations for a username.\n\n"
                                "For example, for the username 'balestek86', the permutations would include:\n"
                                "balestek\n"
                                "_balestek\n"
                                "balestek_\n"
                                "86\n"
                                "_86\n"
                                "86_\n"
                                "balestek86\n"
                                "_balestek86\n"
                                "balestek86_\n"
                                "balestek_86\n"
                                "balestek-86\n"
                                "balestek.86\n"
                                "86balestek\n"
                                "_86balestek\n"
                                "86balestek_\n"
                                "86_balestek\n"
                                "86-balestek\n"
                                "86.balestek\n\n"
                                "You can use '--permuteall' to create these variations and search them.")



    def run_blackbird(self):
        # Ensure any previous worker is stopped before starting a new one
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()

        # Initialize the Blackbird command with the basic parameters
        command = ["python", "blackbird.py"]
        
        # Add username parameters if entered
        if self.username_input.text():
            usernames = [u.strip() for u in self.username_input.text().split(',')]
            for username in usernames:
                command.extend(["-u", username])
            
            # Add permute options if selected
            if len(usernames) == 1:
                if self.permute_checkbox.isChecked():
                    command.append("--permute")
                elif self.permuteall_checkbox.isChecked():
                    command.append("--permuteall")
        
        # Add email parameters if entered
        if self.email_input.text():
            emails = [e.strip() for e in self.email_input.text().split(',')]
            for email in emails:
                command.extend(["-e", email])
        
        # # If a file was selected, append it to the command
        # if self.file_input.text():
        #     if self.username_input.text():
        #         command.extend(["--username-file", self.file_input.text()])
        #     elif self.email_input.text():
        #         command.extend(["--email-file", self.file_input.text()])
        
        # Add other options like excluding NSFW, proxy, timeout, etc.
        if self.no_nsfw_checkbox.isChecked():
            command.append("--no-nsfw")
        
        if self.proxy_input.text():
            command.extend(["--proxy", self.proxy_input.text()])
        
        command.extend(["--timeout", str(self.timeout_spinbox.value())])
        
        if self.no_update_checkbox.isChecked():
            command.append("--no-update")
        
        if self.filter_input.text():
            command.extend(["--filter", self.filter_input.text()])
        
        # Handle output format options
        if self.csv_checkbox.isChecked():
            command.append("--csv")
        
        if self.pdf_checkbox.isChecked():
            command.append("--pdf")
        
        if self.verbose_checkbox.isChecked():
            command.append("--verbose")
        
        if self.dump_checkbox.isChecked():
            command.append("--dump")

        # Set the Instagram session ID environment variable if entered
        if self.instagram_session_id.text():
            os.environ["INSTAGRAM_SESSION_ID"] = self.instagram_session_id.text()

        # Clear previous output and start the worker thread
        self.output_area.clear()
        self.worker = BlackbirdWorker(" ".join(command))
        self.worker.output_signal.connect(self.update_output)  # Connect output signal to update method
        self.worker.finished.connect(self.on_worker_finished)  # Handle when worker finishes
        self.worker.start()
        
        # Disable Run button and enable Stop button during execution
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_blackbird(self):
        # Stop the Blackbird process if running
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        self.run_button.setEnabled(True)  # Re-enable Run button
        self.stop_button.setEnabled(False)  # Disable Stop button

    def update_output(self, text):
        # Update the output area with new text (logs/results)
        scrollbar = self.output_area.verticalScrollBar()
        was_at_bottom = scrollbar.value() == scrollbar.maximum()

        self.output_area.append(text)

        if was_at_bottom:
            scrollbar.setValue(scrollbar.maximum())  # Auto-scroll to the bottom

    def on_worker_finished(self):
        # Re-enable the Run button and disable the Stop button when worker finishes
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == "__main__":
    # Create and run the application
    app = QApplication(sys.argv)
    window = BlackbirdGUI()
    window.show()
    sys.exit(app.exec())
