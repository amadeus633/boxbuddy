import openai
from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.Qt import QApplication

openai.api_key = "YOUR_API_KEY_HERE"

# hackGPT
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a white hat cyber security professional. You specialize in Offensive Security and you are able to explain exploit techniques, vulnerability analysis, scripting, and privelage escalation techniques to students using learning platforms such as Hack The Box."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
        n=1,
        temperature=0.5,
    )

    message = response['choices'][0]['message']['content'].strip()
    return message

class ExpandingInput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(False)  # to prevent pasting of rich text
        self.setMinimumHeight(25)
        self.setMaximumHeight(100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
            self.parent().send_message()  # send the message when Enter is pressed
        else:
            super().keyPressEvent(event)  # default behavior for other keys

# Rest of the code remains the same

class ChatGPTDockWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Chat window
        self.chat_window = QTextEdit(self)
        self.chat_window.setAcceptRichText(False)  # set this to False to get plain text for exporting
        self.chat_window.setReadOnly(True)
        layout.addWidget(self.chat_window)

        # User input
        self.user_input = ExpandingInput()
        layout.addWidget(self.user_input)

        # Button layout
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        button_layout.addWidget(self.send_button)

        # Export conversation button
        self.export_button = QPushButton("Export", self)
        self.export_button.clicked.connect(self.export_conversation)
        button_layout.addWidget(self.export_button)

        self.setLayout(layout)

    def export_conversation(self):
        # Open a QFileDialog in save file mode
        filename, _ = QFileDialog.getSaveFileName(self, "Save conversation", "", "Text Files (*.txt)")
        if filename:
            # If a file was selected, write the chat window's contents to that file
            with open(filename, 'w') as f:
                f.write(self.chat_window.toPlainText())
                           
    def send_message(self):
        user_message = self.user_input.toPlainText().strip()
        if user_message:  # only send non-empty messages
            chatgpt_message = generate_text(user_message)

        # Append the user's message and GPT's response to the chat window
        self.append_message("You", user_message)
        self.append_message("GPT", chatgpt_message)

        # Clear the user input
        self.user_input.clear()

    def append_message(self, sender, message):
        color = "gray" if sender == "You" else "red"
        message = message.replace('\n', '<br>')  # add this line
        self.chat_window.append(f'<b><font color="{color}">{sender}</font></b>: {message}')



    def copy_chatgpt_response(self):
        chatgpt_message = self.chatgpt_response.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(chatgpt_message)
