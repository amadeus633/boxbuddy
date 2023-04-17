#!/usr/bin/python

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QGridLayout,
)
from PyQt5.QtCore import QThreadPool, QRunnable
from PyQt5.QtGui import QIcon  # Add this import
import subprocess
import platform

from tkinter import Tk
from tkinter.filedialog import askopenfilename

class ScriptRunner(QRunnable):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        subprocess.Popen(["qterminal", "-e"] + [" ".join(self.command) + "; read -p 'Press [Enter] to close the terminal...'"])


def run_script1_with_input():
    ip_address = ip_entry.text()
    if not ip_address:
        return
    runner = ScriptRunner(["python", "scripts/nmap.py", ip_address])
    QThreadPool.globalInstance().start(runner)

def run_script2_with_input():
    nip_address = nip_entry.text()
    if not nip_address:
        return
    runner = ScriptRunner(["python", "scripts/nikto.py", nip_address])
    QThreadPool.globalInstance().start(runner)

def run_script3_with_input():
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    runner = ScriptRunner(["python", "scripts/dirsearch.py", ddomain])
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

app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet("styles.css"))

# Set the application icon
icon = QIcon("img/200x200.png")
app.setWindowIcon(icon)

window = QWidget()
window.setWindowTitle("BoxBuddy")
window.setGeometry(100, 100, 250, 300)

layout = QVBoxLayout()
window.setLayout(layout)

tab_widget = QTabWidget()
layout.addWidget(tab_widget)

# Tab 1: Setup commands

filename = 'None selected'

setup_tab = QWidget()
tab_widget.addTab(setup_tab, "Setup")
setup_layout = QVBoxLayout()
setup_tab.setLayout(setup_layout)

file_btn = QPushButton("Select file")
file_btn.clicked.connect(file_select)
setup_layout.addWidget(file_btn)

file_label = QLabel(filename)
setup_layout.addWidget(file_label)

button3 = QPushButton("vpn")
button3.clicked.connect(lambda:run_vpn(filename))
setup_layout.addWidget(button3)

# Add setup tab content here

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

nip_label = QLabel("Please enter the IP address:")
recon_layout.addWidget(nip_label)

nip_entry = QLineEdit()
recon_layout.addWidget(nip_entry)

button2 = QPushButton("nikto")
button2.clicked.connect(run_script2_with_input)
recon_layout.addWidget(button2)

ddomain_label = QLabel("Please enter the domain:")
recon_layout.addWidget(ddomain_label)

ddomain_entry = QLineEdit()
recon_layout.addWidget(ddomain_entry)

button3 = QPushButton("dirsearch")
button3.clicked.connect(run_script3_with_input)
recon_layout.addWidget(button3)

# Tab 3: Automation
automation_tab = QWidget()
tab_widget.addTab(automation_tab, "Automation")
automation_layout = QVBoxLayout()
automation_tab.setLayout(automation_layout)

# Add automation tab content here

window.show()
sys.exit(app.exec_())
