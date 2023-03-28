import sys
from datetime import datetime
import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, \
    QRadioButton, QCheckBox, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QTextEdit, QLineEdit
from PyQt6.QtCore import Qt
import json

from question import questions, Question
from sys_record import SysRecorder
from voice_record import VoiceRecorder


class QuizWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анкета")
        self.setWindowIcon(QIcon('python.ico'))
        self.current_question_index = 0
        self.answers = {}
        self.username = ""
        self.setup_home_page()
        self.voice_recorder = VoiceRecorder()
        self.sys_recorder = SysRecorder()
        date_time_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_date = f'{date_time_string}'

    def start_recording(self):
        self.voice_recorder.start_recording()
        #self.sys_recorder.start_recording()

    def stop_recording(self):
        self.voice_recorder.stop_recording(self.file_date)
        #self.sys_recorder.stop_recording(self.file_date)

    def setup_home_page(self):
        self.setFixedSize(800, 600)
        name_widget = QWidget()
        name_layout = QVBoxLayout(name_widget)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F8F8FF;
            }
            """
        )
        name_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        name_label = QLabel("Выберите пользователя")
        name_label.setStyleSheet("color: black; border-radius: 10px; font: bold 20px")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_edit = QComboBox()
        self.name_edit.addItems(["Пользовать №14124", "Пользовать №41234", "Пользовать №9532"])
        self.name_edit.setStyleSheet("color: black; font: 20px")
        start_button = QPushButton("Принять звонок")
        start_button.setStyleSheet("background-color: #ffa500; color: black; border-radius: 10px; font: bold 20px")
        start_button.clicked.connect(self.start_quiz)
        start_button.clicked.connect(self.start_recording)
        name_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        name_layout.addWidget(self.name_edit, alignment=Qt.AlignmentFlag.AlignCenter)
        name_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        name_widget.setFixedSize(400, 300)
        start_button.setFixedSize(200, 50)
        self.username = self.name_edit.currentText()
        central_layout = QHBoxLayout()
        central_layout.addStretch()
        central_layout.addWidget(name_widget)
        central_layout.addStretch()
        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def start_quiz(self):
        self.username = self.name_edit.currentText()
        if self.username:
            self.setup_ui()
            self.show_question()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F8F8FF;
            }
            """
        )
        self.setFixedSize(800, 600)
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("color: black; border-radius: 10px; font: bold 20px")
        self.answers_widget = QWidget()
        self.answers_layout = QVBoxLayout()
        self.answers_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answers_widget.setStyleSheet("color: black; border-radius: 10px; font: bold 15px")
        self.answers_widget.setLayout(self.answers_layout)
        self.submit_button = QPushButton("Следующий вопрос")
        self.submit_button.setStyleSheet("background-color: #ffa500; color: black; border-radius: 10px; font: bold 20px")
        self.submit_button.setFixedSize(250, 50)
        self.submit_button.clicked.connect(self.submit_answer)
        self.restart_button = QPushButton("Принять новый звонок")
        self.restart_button.setStyleSheet("background-color: #ffff00; color: black; border-radius: 10px; font: bold 15px")
        self.restart_button.setFixedSize(200, 50)
        self.restart_button.clicked.connect(self.restart_quiz)
        self.question_label.setFixedWidth(400)
        self.answers_widget.setFixedWidth(400)
        self.setCentralWidget(QWidget())
        central_layout = QVBoxLayout(self.centralWidget())
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(self.question_label, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(self.answers_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(self.restart_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.restart_button.hide()
        user_info = QLabel(f"Текущий пользователь: {self.username}")
        user_info.setAlignment(Qt.AlignmentFlag.AlignRight)
        central_layout.addWidget(user_info, alignment=Qt.AlignmentFlag.AlignRight)

    def restart_quiz(self):
        date_time_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_date = f'{date_time_string}'
        self.current_question_index = 0
        self.answers = {}
        self.setup_home_page()

    def show_question(self):
        self.current_question = questions[self.current_question_index]
        self.question_label.setText(self.current_question.question_text)
        self.clear_answers()
        if self.current_question.answer_type == "one":
            self.radio_buttons = []
            answer_widget = QHBoxLayout()
            for answer in self.current_question.answers:
                radio_button = QRadioButton(answer)
                answer_widget.addWidget(radio_button)
                self.radio_buttons.append(radio_button)
            self.answers_layout.addLayout(answer_widget)
        elif self.current_question.answer_type == "many":
            self.check_boxes = []
            answer_widget = QHBoxLayout()
            for answer in self.current_question.answers:
                check_box = QCheckBox(answer)
                answer_widget.addWidget(check_box)
                self.check_boxes.append(check_box)
            self.answers_layout.addLayout(answer_widget)
        elif self.current_question.answer_type == "text":
            self.text_edit = QTextEdit()
            self.answers_layout.addWidget(self.text_edit)
        elif self.current_question.answer_type == "table":
            self.table_widget = QTableWidget()
            self.table_widget.setRowCount(3)
            self.table_widget.setColumnCount(3)
            self.table_widget.setFixedSize(600, 300)
            for i in range(3):
                for j in range(3):
                    item = QTableWidgetItem()
                    self.table_widget.setItem(i, j, item)
                    self.table_widget.setColumnWidth(i, 125)
                    self.table_widget.setRowHeight(j, 90)
            self.answers_layout.addWidget(self.table_widget)
        if self.current_question_index == len(questions) - 1:
            self.submit_button.setText("Подвести итоги")

    def clear_answers(self):
        while self.answers_layout.count() > 0:
            item = self.answers_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def submit_answer(self):
        answer_selected = False
        if self.current_question.answer_type == "one":
            for i, radio_button in enumerate(self.radio_buttons):
                if radio_button.isChecked():
                    self.answers[self.current_question_index] = [i]
                    answer_selected = True
                    break
            if not answer_selected:
                QMessageBox.warning(self, "Внимание", "Выберите ответ")
                return
        elif self.current_question.answer_type == "many":
            checked_boxes = []
            for i, check_box in enumerate(self.check_boxes):
                if check_box.isChecked():
                    checked_boxes.append(i)
            if checked_boxes:
                self.answers[self.current_question_index] = checked_boxes
                answer_selected = True
            if not answer_selected:
                QMessageBox.warning(self, "Внимание", "Выберите ответ\ы")
                return
        elif self.current_question.answer_type == "text":
            answer_text = self.text_edit.toPlainText()
            if answer_text:
                self.answers[self.current_question_index] = answer_text
                answer_selected = True
            if not answer_selected:
                QMessageBox.warning(self, "Внимание", "Введите ответ")
                return
        elif self.current_question.answer_type == "table":
            table_answers = []
            for i in range(3):
                row_answers = []
                for j in range(3):
                    item = self.table_widget.item(i, j)
                    if item is not None and item.text():
                        row_answers.append(item.text())
                table_answers.append(row_answers)
            if table_answers:
                self.answers[self.current_question_index] = table_answers
                answer_selected = True
            if not answer_selected:
                QMessageBox.warning(self, "Внимание", "Заполните таблицу")
                return
        self.current_question_index += 1
        if self.current_question_index == len(questions):
            self.show_results()
        else:
            self.show_question()

    def save_results(self):
        results = {}
        current_user_answers = []
        for question_index, answer in self.answers.items():
            current_question = questions[question_index]
            question_text = current_question.question_text
            answer_text = ""
            if current_question.answer_type == "one":
                answer_text = current_question.answers[answer[0]]
            elif current_question.answer_type == "many":
                answer_text = ", ".join([current_question.answers[i] for i in answer])
            elif current_question.answer_type == "text":
                answer_text = self.text_edit.toPlainText()
            elif current_question.answer_type == "table":
                table_data = []
                for i in range(self.table_widget.rowCount()):
                    row_data = []
                    for j in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(i, j)
                        if item is not None and item.text():
                            row_data.append(item.text())
                    table_data.append(row_data)
                answer_text = json.dumps(table_data)
            current_user_answers.append([question_text, answer_text])

        results[self.username] = current_user_answers

        filename = f"{self.file_date}_results.json"
        output_path = 'questionnaires'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_filename = os.path.join(output_path, filename)
        with open(output_filename, "w") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)

        QMessageBox.information(self, "Результат", f"Результаты сохранены в файл {filename}")

    def show_results(self):
        self.clear_answers()
        self.restart_button.show()
        result_widget = QWidget()
        result_layout = QVBoxLayout()
        result_widget.setLayout(result_layout)
        title_label = QLabel("Анкета")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: black; border-radius: 10px; font: bold 20px")
        result_layout.addWidget(title_label)

        user_info = QLabel(f"Текущий пользователь: {self.username}")
        user_info.setAlignment(Qt.AlignmentFlag.AlignRight)
        result_layout.addWidget(user_info)

        string_result = ""
        for i, question in enumerate(questions):
            if question.answer_type in ["one", "many"]:
                string_result += f"{i + 1}. {question.question_text}\n"
                user_answer = self.answers.get(i)
                if user_answer is not None:
                    for answer_index in user_answer:
                        string_result += f"- {question.answers[answer_index]}\n"
                else:
                    string_result += "- Нет ответа\n"
        if string_result:
            string_result_widget = QTextEdit()
            string_result_widget.setReadOnly(True)
            string_result_widget.setText(string_result)
            result_layout.addWidget(string_result_widget)

        text_result = ""
        for i, question in enumerate(questions):
            if question.answer_type == "text":
                text_result += f"{i + 1}. {question.question_text}\n"
                user_answer = self.answers.get(i)
                if user_answer is not None:
                    text_result += f"- {user_answer}\n"
                else:
                    text_result += "- Нет ответа\n"
        if text_result:
            text_result_widget = QTextEdit()
            text_result_widget.setReadOnly(True)
            text_result_widget.setText(text_result)
            result_layout.addWidget(text_result_widget)

        table_result = []
        for i, question in enumerate(questions):
            if question.answer_type == "table":
                table_result.append([question.question_text])
                user_answer = self.answers.get(i)
                if user_answer is not None:
                    for row in user_answer:
                        table_result[-1].append(row)
                else:
                    table_result[-1].append("Нет ответа")
        if table_result:
            table_result_widget = QTableWidget()
            table_result_widget.setRowCount(len(table_result))
            table_result_widget.setColumnCount(len(table_result[0]))
            for i, row in enumerate(table_result):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                    table_result_widget.setItem(i, j, item)
                    table_result_widget.setRowHeight(i, 100)
                    table_result_widget.setColumnWidth(j, 100)
            result_layout.addWidget(table_result_widget)
        self.setCentralWidget(result_widget)

        self.save_results()
        self.stop_recording()
        result_layout.addWidget(self.restart_button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuizWindow()
    window.show()
    sys.exit(app.exec())