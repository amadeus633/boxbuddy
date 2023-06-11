from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
import os
import json

class NotesWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.note_file = "notes.json"

        self.notes = QTextEdit()
        self.notes.textChanged.connect(self.save_notes)

        self.export_button = QPushButton("Export Notes")
        self.export_button.clicked.connect(self.export_notes)

        layout = QVBoxLayout()
        layout.addWidget(self.notes)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.note_file):
            with open(self.note_file, "r") as file:
                notes_content = json.load(file)
                self.notes.setText(notes_content.get('notes', ''))

    def save_notes(self):
        notes_content = self.notes.toPlainText()
        with open(self.note_file, "w") as file:
            json.dump({'notes': notes_content}, file)

    def export_notes(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Notes", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "w") as file:
                file.write(self.notes.toPlainText())
