import stanza
import sys
from PySide2 import QtWidgets, QtGui, QtCore

class StanzaNLPApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TamilPOS Using Stanza")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QtWidgets.QVBoxLayout()

        self.create_menu()

        self.input_text_widget = QtWidgets.QTextEdit(self)
        self.input_text_widget.setStyleSheet("background-color: #FFFFE0;")
        self.input_text_widget.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.input_text_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        layout.addWidget(self.input_text_widget)

        self.output_text_widget = QtWidgets.QTextEdit(self)
        self.output_text_widget.setStyleSheet("background-color: #E0FFFF;")
        self.output_text_widget.setReadOnly(True)
        self.output_text_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        layout.addWidget(self.output_text_widget)

        self.central_widget.setLayout(layout)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("கோப்பு")
        process_action = QtWidgets.QAction("குறியிடப்பட வேண்டிய கோப்பு", self)
        process_action.triggered.connect(self.process_file)
        file_menu.addAction(process_action)

        exit_action = QtWidgets.QAction("வெளியேறு", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("உதவி")
        about_action = QtWidgets.QAction("பற்றி", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)


    def process_and_save(self, input_text, output_file):
        config = {
            'processors': 'tokenize,pos',
            'lang': 'ta',
        }
        nlp = stanza.Pipeline(**config)
        doc = nlp(input_text)

        with open(output_file, 'w', encoding='utf-8') as f_out:
            for sentence in doc.sentences:
                for word in sentence.words:
                    f_out.write(f"{word.text},  {word.upos}\n")

        self.show_end_message()
        self.show_output_results(doc)

    def process_file(self):
        input_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Input File", "", "Text Files (*.txt)")
        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f_in:
                input_text = f_in.read()
                self.input_text_widget.setPlainText(input_text)

            output_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Select Output File", "", "Text Files (*.txt)")
            if output_file:
                self.process_and_save(input_text, output_file)

    def show_end_message(self):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Process Completed")
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText("The process has been completed.")
        msg_box.exec_()

    def show_output_results(self, doc):
        output_text = ""
        for sentence in doc.sentences:
            for word in sentence.words:
                output_text += f" {word.text}   {word.upos}\n"
        self.output_text_widget.setPlainText(output_text)

    def show_about_dialog(self):
        about_text = "TamilPOS Using Stanza\nகுறியாக்கம்: ஜெஸ்மன் பிள்ளை\n(C) 2023 "
        QtWidgets.QMessageBox.about(self, "About", about_text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = StanzaNLPApp()
    main_win.show()
    sys.exit(app.exec_())

