#!/usr/bin/python
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QLabel, QHBoxLayout, QScrollArea, QFrame
)
from PyQt5.Qt import QApplication

class CopyPasteTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.targeturl_entry = QLineEdit()
        self.ipaddress_entry = QLineEdit()
        form_layout.addRow("Target URL:", self.targeturl_entry)
        form_layout.addRow("IP address:", self.ipaddress_entry)

        submit_button = QPushButton("Replace")
        submit_button.clicked.connect(self.on_submit)
        form_layout.addRow(submit_button)

        layout.addLayout(form_layout)

        line = QLabel()
        line.setFrameShape(QLabel.HLine)
        line.setFrameShadow(QLabel.Sunken)
        layout.addWidget(line)

        self.sections = [
            ("NMAP:", [
                "nmap -sC -sV -Pn -p- ipaddress",
                "COMMAND"
            ]),
            ("NIKTO", [
                "nikto -h ipaddress",
                "COMMAND"
            ]),
            ("GOBUSTER", [
                "COMMAND",
                "COMMAND"
            ]),
            ("DIRB", [
                "nikto -h ipaddress",
                "COMMAND"
            ]),
            ("FFUZ", [
                "COMMAND",
                "COMMAND"
            ]),
            ("RUSTSCAN", [
                "nikto -h ipaddress",
                "COMMAND"
            ]),
            ("Section 1:", [
                "COMMAND",
                "COMMAND"
            ]),
            ("Section 2:", [
                "nikto -h ipaddress",
                "COMMAND"
            ]),
            ("Section 1:", [
                "COMMAND",
                "COMMAND"
            ]),
            ("Section 2:", [
                "nikto -h ipaddress",
                "COMMAND"
            ]),
            # Add more sections as needed
        ]

        # Create a scrollable area and put your layout inside
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        content_layout = QVBoxLayout(content_widget)
        self.add_sentences_with_subheadings(content_layout)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)

    def add_sentences_with_subheadings(self, layout):
        self.buttons = []
        self.labels = []

        for section_title, sentences in self.sections:
            subheading = QLabel(section_title)
            layout.addWidget(subheading)

            for sentence in sentences:
                button = QPushButton("Copy")
                button.clicked.connect(self.copy_to_clipboard)
                label = QLabel(sentence)
                sentence_layout = QHBoxLayout()
                sentence_layout.addWidget(button)
                sentence_layout.addWidget(label)
                layout.addLayout(sentence_layout)
                self.buttons.append(button)
                self.labels.append(label)

    def on_submit(self):
        ipaddress = self.ipaddress_entry.text()
        domain = self.targeturl_entry.text()

        index = 0
        for section_title, sentences in self.sections:
            for sentence in sentences:
                updated_sentence = sentence.replace("ipaddress", ipaddress).replace("htbdomain", domain)
                self.labels[index].setText(updated_sentence)
                index += 1

    def copy_to_clipboard(self):
        index = self.buttons.index(self.sender())
        text = self.labels[index].text()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
