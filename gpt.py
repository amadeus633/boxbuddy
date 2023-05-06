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
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.QtWebEngineWidgets import QWebEngineView
import subprocess
import platform
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import openai
openai.api_key = "KEY"


class ScriptRunnerSignals(QObject):
    output_ready = pyqtSignal(str, str, str)

class ScriptRunner(QRunnable):

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.signals = ScriptRunnerSignals()

    def run(self):
        if platform.system() == "Windows":
            result = subprocess.run(
                ["cmd.exe", "/k"] + self.command,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                capture_output=True,
            )
        elif platform.system() == "Linux":
            shell = "zsh"
            result = subprocess.run(["exo-open", "--launch", "TerminalEmulator"] + [shell, "-c", " ".join(self.command) + "; exec " + shell], capture_output=True)
        else:
            result = subprocess.run(["qterminal", "-e"] + [" ".join(self.command)], capture_output=True)

        stdout, stderr = result.stdout, result.stderr
        self.signals.output_ready.emit(f"Command: {self.command}", stdout.decode(), stderr.decode())

def update_output_widget(command, stdout, stderr):
    output_widget.append(command)
    output_widget.append("STDOUT:")
    output_widget.append(stdout)
    output_widget.append("STDERR:")
    output_widget.append(stderr)

def run_script1_with_input(output_widget):
    ip_address = ip_entry.text()
    if not ip_address:
        return
    runner = ScriptRunner(["python", "scripts/nmap.py", ip_address])
    runner.signals.output_ready.connect(update_output_widget)
    QThreadPool.globalInstance().start(runner)

# ... (The rest of your script remains the same)

# In each function where you create a ScriptRunner instance, connect the output_ready signal to the update_output_widget slot:
# runner.signals.output_ready.connect(update_output_widget)


def run_nikto(output_widget):
    ip_address = ip_entry.text()
    if not ip_address:
        return
    runner = ScriptRunner(["python", "scripts/nikto.py", ip_address])
    runner.signals.output_ready.connect(update_output_widget)
    QThreadPool.globalInstance().start(runner)

def run_dirsearch(output_widget):
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    runner = ScriptRunner(["python", "scripts/dirsearch.py", ddomain])
    runner.signals.output_ready.connect(update_output_widget)
    QThreadPool.globalInstance().start(runner)

def run_gobuster_vhost(output_widget):
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    runner = ScriptRunner(["python", "scripts/gobuster-vhost.py", ddomain])
    runner.signals.output_ready.connect(update_output_widget)
    QThreadPool.globalInstance().start(runner)

def run_gobuster_dir(output_widget):
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    runner = ScriptRunner(["python", "scripts/gobuster-dir.py", ddomain])
    runner.signals.output_ready.connect(update_output_widget)
    QThreadPool.globalInstance().start(runner)

def run_vpn(file):
    runner = ScriptRunner(["python", "scripts/vpn.py", f"{file}"])
    QThreadPool.globalInstance().start(runner)

def load_stylesheet(file_path):
    with open(file_path, "r") as file:
        return file.read()
        
def file_select():
    global filename
    Tk().withdraw()
    filename = askopenfilename()
    file_label.setText(filename.split('/')[-1])

# def run_hosts():
#     ddomain = ddomain_entry.text()
#     if not ddomain:
#         return
#     ip_address = ip_entry.text()
#     if not ip_address:
#         return
#     runner = ScriptRunner(["python", "scripts/hosts.py", ip_address, ddomain])
#     QThreadPool.globalInstance().start(runner)
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

# window size
window = QWidget()
window.setWindowTitle("BoxBuddy")
window.setGeometry(100, 100, 700, 500)

layout = QVBoxLayout()
window.setLayout(layout)

tab_widget = QTabWidget()
layout.addWidget(tab_widget)
#
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
button3.clicked.connect(lambda:run_vpn(filename))
setup_layout.addWidget(button3)

# ip_label = QLabel("Please enter the IP address:")
# setup_layout.addWidget(ip_label)

# ip_entry = QLineEdit()
# setup_layout.addWidget(ip_entry)

# ddomain_label = QLabel("Please enter the domain:")
# setup_layout.addWidget(ddomain_label)

# ddomain_entry = QLineEdit()
# setup_layout.addWidget(ddomain_entry)

# button4 = QPushButton("Add to etc/hosts")
# button4.clicked.connect(run_hosts)
# setup_layout.addWidget(button4)
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
button1.clicked.connect(run_script1_with_input)
recon_layout.addWidget(button1)

button2 = QPushButton("nikto")
button2.clicked.connect(run_nikto)
recon_layout.addWidget(button2)

ddomain_label = QLabel("Please enter the domain:")
recon_layout.addWidget(ddomain_label)

ddomain_entry = QLineEdit()
recon_layout.addWidget(ddomain_entry)

button3 = QPushButton("dirsearch")
button3.clicked.connect(run_dirsearch)
recon_layout.addWidget(button3)

button4 = QPushButton("gobuster - vhost")
button4.clicked.connect(run_gobuster_vhost)
recon_layout.addWidget(button4)

button5 = QPushButton("gobuster - dir")
button5.clicked.connect(run_gobuster_dir)
recon_layout.addWidget(button5)

feed_label = QLabel("Feed (loads after closing terminal window)")
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
# Tab 3: CopyPaste

class CopyPasteTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.domain_entry = QLineEdit()
        self.ipaddress_entry = QLineEdit()
        form_layout.addRow("Domain:", self.domain_entry)
        form_layout.addRow("IP address:", self.ipaddress_entry)

        submit_button = QPushButton("Replace")
        submit_button.clicked.connect(self.on_submit)
        form_layout.addRow(submit_button)

        layout.addLayout(form_layout)

        line = QLabel()
        line.setFrameShape(QLabel.HLine)
        line.setFrameShadow(QLabel.Sunken)
        layout.addWidget(line)

        self.sentences = [
            "nmap -sC -sV -Pn -p- ipaddress",
            "dirb http://ipaddress /usr/share/dirb/wordlists/common.txt -X .htbdomain",
            "nikto -h ipaddress",
            "Sed do eiusmod ipaddress tempor incididunt.",
            "Sed do eiusmod ipaddress tempor incididunt.",
            "Sed do eiusmod ipaddress tempor incididunt.",
            "Sed do eiusmod ipaddress tempor incididunt."
        ]

        self.buttons = []
        self.labels = []

        for sentence in self.sentences:
            button = QPushButton("Copy")
            button.clicked.connect(self.copy_to_clipboard)
            label = QLabel(sentence)
            sentence_layout = QHBoxLayout()
            sentence_layout.addWidget(button)
            sentence_layout.addWidget(label)
            layout.addLayout(sentence_layout)
            self.buttons.append(button)
            self.labels.append(label)

        self.setLayout(layout)

    def on_submit(self):
        ipaddress = self.ipaddress_entry.text()
        domain = self.domain_entry.text()

        for i, sentence in enumerate(self.sentences):
            updated_sentence = sentence.replace("ipaddress", ipaddress).replace("htbdomain", domain)
            self.labels[i].setText(updated_sentence)

    def copy_to_clipboard(self):
        index = self.buttons.index(self.sender())
        text = self.labels[index].text()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
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

window.show()
sys.exit(app.exec_())
