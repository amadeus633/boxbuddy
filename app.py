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
    QTextEdit,  
)
from PyQt5.QtCore import QThreadPool, QRunnable
from PyQt5.QtGui import QIcon  
import subprocess
import platform
from tkinter import Tk
from tkinter.filedialog import askopenfilename
#
#
#
class ScriptRunner(QRunnable):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        if platform.system() == "Windows":
            subprocess.Popen(
                ["cmd.exe", "/k"] + self.command,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
        elif platform.system() == "Linux":
            shell = "zsh"  # Change this to "bash" if you prefer bash

            # Example using exo-open
            subprocess.Popen(["exo-open", "--launch", "TerminalEmulator"] + [shell, "-c", " ".join(self.command) + "; exec " + shell])
        else:
            subprocess.Popen(["qterminal", "-e"] + [" ".join(self.command)])

        # Update the output widget with the results
        output_widget.append(f"Command: {self.command}")
        output_widget.append("STDOUT:")
        output_widget.append(stdout.decode())
        output_widget.append("STDERR:")
        output_widget.append(stderr.decode())

def run_script1_with_input(output_widget):
    ip_address = ip_entry.text()
    if not ip_address:
        return
    runner = ScriptRunner(["python", "scripts/nmap.py", ip_address])
    runner.signals.finished.connect(lambda: output_widget.append("Finished running script1"))
    QThreadPool.globalInstance().start(runner)

def run_nikto(output_widget):
    ip_address = ip_entry.text()
    if not ip_address:
        return
    runner = ScriptRunner(["python", "scripts/nikto.py", ip_address])
    runner.signals.finished.connect(lambda: output_widget.append("Finished running script1"))
    QThreadPool.globalInstance().start(runner)

def run_dirsearch(output_widget):
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    runner = ScriptRunner(["python", "scripts/dirsearch.py", ddomain])
    runner.signals.finished.connect(lambda: output_widget.append("Finished running script1"))
    QThreadPool.globalInstance().start(runner)

def run_gobuster_vhost(output_widget):
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    runner = ScriptRunner(["python", "scripts/gobuster-vhost.py", ddomain])
    runner.signals.finished.connect(lambda: output_widget.append("Finished running script1"))
    QThreadPool.globalInstance().start(runner)

def run_gobuster_dir(output_widget):
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    runner = ScriptRunner(["python", "scripts/gobuster-dir.py", ddomain])
    runner.signals.finished.connect(lambda: output_widget.append("Finished running script1"))
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

def run_hosts():
    ddomain = ddomain_entry.text()
    if not ddomain:
        return
    ip_address = ip_entry.text()
    if not ip_address:
        return
    runner = ScriptRunner(["python", "scripts/hosts.py", ip_address, ddomain])
    QThreadPool.globalInstance().start(runner)
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
window.setGeometry(100, 100, 250, 300)

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

ip_label = QLabel("Please enter the IP address:")
setup_layout.addWidget(ip_label)

ip_entry = QLineEdit()
setup_layout.addWidget(ip_entry)

ddomain_label = QLabel("Please enter the domain:")
setup_layout.addWidget(ddomain_label)

ddomain_entry = QLineEdit()
setup_layout.addWidget(ddomain_entry)

button4 = QPushButton("Add to etc/hosts")
button4.clicked.connect(run_hosts)
setup_layout.addWidget(button4)
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
# Tab 3: Automation
automation_tab = QWidget()
tab_widget.addTab(automation_tab, "Automation")
automation_layout = QVBoxLayout()
automation_tab.setLayout(automation_layout)
#
#
#
#
#

window.show()
sys.exit(app.exec_())
