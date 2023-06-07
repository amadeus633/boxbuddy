#!/usr/bin/python

import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QFormLayout,
    QHBoxLayout,
    QFileDialog
)
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.QtWebEngineWidgets import QWebEngineView
import subprocess
import platform
from scripts.copypaste import CopyPasteTab
from notes import NotesWidget
import openai
openai.api_key = "OPENAI_API_KEY"


class ScriptRunnerSignals(QObject):
    output_ready = pyqtSignal(str, str, str)

class ScriptRunner(QRunnable):

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.signals = ScriptRunnerSignals()

    def run(self):
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )

        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                self.signals.output_ready.emit(f"-", output.strip(), "")

        while True:
            output = process.stderr.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                self.signals.output_ready.emit(f"-", "", output.strip())

def append_output(prefix, stdout, stderr):
    if stdout:
        output_widget.append(f"{prefix} {stdout}")
    if stderr:
        output_widget.append(f"{prefix} {stderr}")

def run_nmap(output_widget):
    ip_address = ip_entry.text()
    if not ip_address:
        return
    script_path = os.path.join("", "scripts", "nmap.py")
    runner = ScriptRunner(["python", script_path, ip_address])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

def run_nikto(output_widget):
    ip_address = ip_entry.text()
    if not ip_address:
        return
    script_path = os.path.join("", "scripts", "nikto.py")
    runner = ScriptRunner(["python", script_path, ip_address])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

def run_dirsearch(output_widget):
    targeturl = targeturl_entry.text()
    if not targeturl:
        return
    script_path = os.path.join("", "scripts", "dirsearch.py")
    runner = ScriptRunner(["python", script_path, targeturl])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

def run_gobuster_vhost(output_widget):
    domain = targeturl_entry.text()
    if not domain:
        return
    script_path = os.path.join("", "scripts", "gobuster_vhost.py")
    runner = ScriptRunner(["python", script_path, domain])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

def run_gobuster_dir(output_widget):
    targeturl = targeturl_entry.text()
    if not targeturl:
        return
    script_path = os.path.join("", "scripts", "gobuster_dir.py")
    runner = ScriptRunner(["python", script_path, targeturl])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

def run_gobuster_dns(output_widget):
    targeturl = targeturl_entry.text()
    if not targeturl:
        return
    script_path = os.path.join("", "scripts", "gobuster_dns.py")
    runner = ScriptRunner(["python", script_path, targeturl])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

def run_vpn(file):
    runner = ScriptRunner(["python", "scripts/vpn.py", f"{file}"])
    QThreadPool.globalInstance().start(runner)


def load_stylesheet(file_path):
    with open(file_path, "r") as file:
        return file.read()
        
def file_select():
    global filename
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    filename, _ = QFileDialog.getOpenFileName(window, "Select File", "", "All Files (*)", options=options)
    if filename:
        file_label.setText(filename.split('/')[-1])
#
#
#
# hackGPT
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
        n=1,
        temperature=0.5,
    )

    message = response['choices'][0]['message']['content'].strip()
    return message
#
#
#
# Personal CLI
class CLITab(QWidget):
    def __init__(self, parent=None):
        super(CLITab, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        web_engine_view = QWebEngineView()

        # Get the absolute path for the index.html file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        index_file_path = os.path.join(current_dir, "cli", "index.html")

        web_engine_view.load(QUrl.fromLocalFile(index_file_path))

        layout = QVBoxLayout(self)
        layout.addWidget(web_engine_view)   
#
#
#
#
#
app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet("styles.css"))

# application icon
icon = QIcon("img/200x200.png")
app.setWindowIcon(icon)

# Create a QMainWindow
window = QMainWindow()
window.setWindowTitle("BoxBuddy")
window.setGeometry(100, 100, 700, 900)

central_widget = QWidget()
layout = QVBoxLayout()
central_widget.setLayout(layout)
window.setCentralWidget(central_widget)

tab_widget = QTabWidget()
layout.addWidget(tab_widget)
#
#
#
#
# Tab 1: Setup commands

setup_tab = QWidget()
tab_widget.addTab(setup_tab, "Setup")
setup_layout = QVBoxLayout()
setup_tab.setLayout(setup_layout)

file_btn = QPushButton("Select file")
file_btn.clicked.connect(file_select)
setup_layout.addWidget(file_btn)

filename = 'None selected'

file_label = QLabel(filename)
setup_layout.addWidget(file_label)

button3 = QPushButton("vpn")
button3.clicked.connect(lambda: run_vpn(filename))
setup_layout.addWidget(button3)
#
#
#
#
#
# Tab 2: Recon commands
recon_tab = QWidget()
tab_widget.addTab(recon_tab, "Recon")
recon_layout = QVBoxLayout()
recon_tab.setLayout(recon_layout)

ip_label = QLabel("Please enter the IP address:")
recon_layout.addWidget(ip_label)

ip_entry = QLineEdit()
recon_layout.addWidget(ip_entry)

button1 = QPushButton("nmap")
button1.clicked.connect(run_nmap)
recon_layout.addWidget(button1)

button2 = QPushButton("nikto")
button2.clicked.connect(run_nikto)
recon_layout.addWidget(button2)

domain_label = QLabel("Please enter the target URL:")
recon_layout.addWidget(domain_label)

targeturl_entry = QLineEdit()
recon_layout.addWidget(targeturl_entry)

button3 = QPushButton("dirsearch")
button3.clicked.connect(run_dirsearch)
recon_layout.addWidget(button3)

button4 = QPushButton("gobuster - vhost")
button4.clicked.connect(run_gobuster_vhost)
recon_layout.addWidget(button4)

button5 = QPushButton("gobuster - dir")
button5.clicked.connect(run_gobuster_dir)
recon_layout.addWidget(button5)

button6 = QPushButton("gobuster - dns")
button6.clicked.connect(run_gobuster_dns)
recon_layout.addWidget(button6)

feed_label = QLabel("Feed")
recon_layout.addWidget(feed_label)
output_widget = QTextEdit()
output_widget.setReadOnly(True)
recon_layout.addWidget(output_widget)

def save_to_file():
    filename, _ = QFileDialog.getSaveFileName(window, "Save Output", "", "Text Files (*.txt)")
    if filename:
        with open(filename, "w") as f:
            f.write(output_widget.toPlainText())

save_button = QPushButton("Save to File")
save_button.clicked.connect(save_to_file)
recon_layout.addWidget(save_button) 
#
#
#
#
#


CopyPaste_tab = CopyPasteTab()
tab_widget.addTab(CopyPaste_tab, "CopyPaste")

class ChatGPTTab(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # User input
        layout.addWidget(QLabel("Your message:"))
        self.user_input = QTextEdit(self)
        layout.addWidget(self.user_input)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)
        
        # ChatGPT response
        layout.addWidget(QLabel("Response:"))
        
        self.chatgpt_response = QTextEdit(self)
        self.chatgpt_response.setReadOnly(True)
        layout.addWidget(self.chatgpt_response)

        # Copy button
        self.copy_button = QPushButton("Copy", self)
        self.copy_button.clicked.connect(self.copy_chatgpt_response)
        layout.addWidget(self.copy_button)
        
        self.setLayout(layout)


    def send_message(self):
        user_message = self.user_input.toPlainText()
        chatgpt_message = generate_text(user_message)
        self.chatgpt_response.setPlainText(chatgpt_message)

    def copy_chatgpt_response(self):
        chatgpt_message = self.chatgpt_response.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(chatgpt_message)
#
#
#
hackGPT_tab = ChatGPTTab()
tab_widget.addTab(hackGPT_tab, "hackGPT")
#
#
#
cli_tab = CLITab()
tab_widget.addTab(cli_tab, "CLI")
#
#
#
notes_widget = NotesWidget()
notes_dock = QDockWidget("Notes", window)
notes_dock.setWidget(notes_widget)
window.addDockWidget(Qt.RightDockWidgetArea, notes_dock)

notes_dock_button = QPushButton("Toggle Notes", central_widget)
notes_dock_button.clicked.connect(notes_dock.toggleViewAction().trigger)
layout.addWidget(notes_dock_button)

window.show()
sys.exit(app.exec_())
