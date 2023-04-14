#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import subprocess

def run_script1_with_input():
    ip_address = ip_entry.text()
    if not ip_address:
        return
    subprocess.run(["python", "scripts/nmap.py", ip_address])

def run_script2():
    subprocess.run(["python", "scripts/recon.py", ip_address])

def run_gobuster():
    domain = domain_entry.text()
    if not domain:
        return
    subprocess.run(["python", "scripts/gobuster.py", domain])

def run_vpn():
    subprocess.run(["python", "scripts/vpn.py", ip_address])

def load_stylesheet(file_path):
    with open(file_path, "r") as file:
        return file.read()

app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet("styles.css"))

window = QWidget()
window.setWindowTitle("BoxBuddy")
window.setGeometry(100, 100, 250, 300)
layout = QVBoxLayout()

layout.setContentsMargins(0, 0, 0, 0)  # Set layout margins
layout.setSpacing(10)  # Set layout spacing

ip_label = QLabel("Please enter the IP address:")
layout.addWidget(ip_label)
ip_entry = QLineEdit()
layout.addWidget(ip_entry)

button1 = QPushButton("nmap")
button1.clicked.connect(run_script1_with_input)
layout.addWidget(button1)

domain_label = QLabel("Please enter the Domain:")
layout.addWidget(domain_label)

domain_entry = QLineEdit()
layout.addWidget(domain_entry)

button2 = QPushButton("gobuster")
button2.clicked.connect(run_gobuster)
layout.addWidget(button2)

button3 = QPushButton("vpn")
button3.clicked.connect(run_vpn)
layout.addWidget(button3)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
