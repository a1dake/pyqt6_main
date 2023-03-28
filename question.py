class Question:
    def __init__(self, question_text, answers, answer_type):
        self.question_text = question_text
        self.answers = answers
        self.answer_type = answer_type

questions = [
    Question("Выберите правильный ответ:", ["Ответ 1", "Ответ 2", "Ответ 3", "Ответ 4"], "one"),
    Question("Выберите все правильные ответы:", ["Ответ 1", "Ответ 2", "Ответ 3", "Ответ 4"], "many"),
    Question("Введите ответ:", [], "text"),
    Question("Выберите ответы для каждой строки:", [["Ответ 1", "Ответ 2", "Ответ 3"], ["Ответ 4", "Ответ 5", "Ответ 6"], ["Ответ 7", "Ответ 8", "Ответ 9"]], "table")
]
