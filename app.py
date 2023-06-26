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
import subprocess
import platform
from scripts.copypaste import CopyPasteTab
from notes import NotesWidget
from chatgpt import ChatGPTDockWidget
import openai



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

# def run_dirsearch(output_widget):
#     targetdomain = domain_entry.text()
#     if not targetdomain:
#         return
#     script_path = os.path.join("", "scripts", "dirsearch.py")
#     runner = ScriptRunner(["python", script_path, targetdomain])
#     runner.signals.output_ready.connect(append_output)
#     QThreadPool.globalInstance().start(runner)

def run_ffuf_directories(output_widget):
    targetdomain = domain_entry.text()
    if not targetdomain:
        return
    script_path = os.path.join("", "scripts", "ffuf_dir.py")
    runner = ScriptRunner(["python", script_path, targetdomain])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

def run_ffuf_subdomains(output_widget):
    targetdomain = domain_entry.text()
    if not targetdomain:
        return
    script_path = os.path.join("", "scripts", "ffuf_subs.py")
    runner = ScriptRunner(["python", script_path, targetdomain])
    runner.signals.output_ready.connect(append_output)
    QThreadPool.globalInstance().start(runner)

# def run_gobuster_dns(output_widget):
#     targetdomain = domain_entry.text()
#     if not targetdomain:
#         return
#     script_path = os.path.join("", "scripts", "gobuster_dns.py")
#     runner = ScriptRunner(["python", script_path, targetdomain])
#     runner.signals.output_ready.connect(append_output)
#     QThreadPool.globalInstance().start(runner)

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
# # hackGPT
# def generate_text(prompt):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt},
#         ],
#         max_tokens=2000,
#         n=1,
#         temperature=0.5,
#     )

#     message = response['choices'][0]['message']['content'].strip()
#     return message
#
#
#
# Personal CLI
# class CLITab(QWidget):
#     def __init__(self, parent=None):
#         super(CLITab, self).__init__(parent)
#         self.init_ui()

#     def init_ui(self):
#         web_engine_view = QWebEngineView()

#         # Get the absolute path for the index.html file
#         current_dir = os.path.dirname(os.path.realpath(__file__))
#         index_file_path = os.path.join(current_dir, "cli", "index.html")

#         web_engine_view.load(QUrl.fromLocalFile(index_file_path))

#         layout = QVBoxLayout(self)
#         layout.addWidget(web_engine_view)   
# #
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
setup_tab..setToolTip("Select your .ovpn file and run command to connect")  # Set tooltip here
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
tab_widget.addTab(recon_tab, "Run")
recon_layout = QVBoxLayout()
recon_tab.setLayout(recon_layout)

ip_label = QLabel("Please enter the IP address:")
recon_layout.addWidget(ip_label)

ip_entry = QLineEdit()
recon_layout.addWidget(ip_entry)

button1 = QPushButton("nmap")
button1.setToolTip("Run nmap scan using the following command: nmap -sC -sV -Pn -p- enteredipaddress")  # Set tooltip here
button1.clicked.connect(run_nmap)
recon_layout.addWidget(button1)

button2 = QPushButton("nikto")
button2.setToolTip("This button will start nikto")  # Set tooltip here
button2.clicked.connect(run_nikto)
recon_layout.addWidget(button2)

domain_label = QLabel("Please enter the target domain (ex. 'boxname.htb'):")
recon_layout.addWidget(domain_label)

domain_entry = QLineEdit()
recon_layout.addWidget(domain_entry)

# button3 = QPushButton("dirsearch")
# button3.clicked.connect(run_dirsearch)
# recon_layout.addWidget(button3)

button4 = QPushButton("ffuf - directories")
button4.clicked.connect(run_ffuf_directories)
recon_layout.addWidget(button4)

button5 = QPushButton("ffuf - subdomains")
button5.clicked.connect(run_ffuf_subdomains)
recon_layout.addWidget(button5)

# button6 = QPushButton("gobuster - dns")
# button6.clicked.connect(run_gobuster_dns)
# recon_layout.addWidget(button6)

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
tab_widget.addTab(CopyPaste_tab, "Copy")


# Create the ChatGPTDockWidget and dock it to the main window
chatgpt_widget = ChatGPTDockWidget()
chatgpt_dock = QDockWidget("hackGPT", window)
chatgpt_dock.setWidget(chatgpt_widget)
window.addDockWidget(Qt.RightDockWidgetArea, chatgpt_dock)
chatgpt_dock.hide()

# Create a button to toggle the ChatGPT dock
chatgpt_dock_button = QPushButton("ChatGPT", central_widget)
chatgpt_dock_button.clicked.connect(chatgpt_dock.toggleViewAction().trigger)

# Add the button to the layout
layout.addWidget(chatgpt_dock_button)


#
#
#
# cli_tab = CLITab()
# tab_widget.addTab(cli_tab, "CLI")
#
#
#
notes_widget = NotesWidget()
notes_dock = QDockWidget("Notes", window)
notes_dock.setWidget(notes_widget)
window.addDockWidget(Qt.BottomDockWidgetArea, notes_dock)

notes_dock_button = QPushButton("Notes", central_widget)
notes_dock_button.clicked.connect(notes_dock.toggleViewAction().trigger)
layout.addWidget(notes_dock_button)




window.show()
sys.exit(app.exec_())
