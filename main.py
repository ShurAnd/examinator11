from tkinter import *

class Question:
    def __init__(self,
                 identifier: int,
                 is_text: bool,
                 question_text: str,
                 text_answer: str,
                 variants: list[str],
                 right_variants: list[bool]):
        self.identifier = identifier
        self.variants = variants
        self.right_variants = right_variants
        self.is_text = is_text
        self.question_text = question_text
        self.text_answer = text_answer

def load_questions():
    q1 = Question(
        1,
        False,
        "Назовите правильный вариант: ",
        "",
        variants=["Варинат 1", "Вариант 2", "Вариант 3", "Вариант 4"],
        right_variants=[False, False, True, False]
    )

    q2 = Question(
        2,
        True,
        "Человек называется _______",
        "Ты",
        variants=[],
        right_variants=[]
    )

    return [q1, q2]

# Настройка весов для столбцов
#root.grid_columnconfigure(0, weight=1)  # Первый столбец + второй (объединенный)
#root.grid_columnconfigure(1, weight=0)  # Второй столбец (не используется отдельно)

class QuizApp:
    question_frame: Frame
    answer_button: Button
    check_button: Button
    result_label: Label
    text_answer: Entry
    check_variants: list[BooleanVar]
    def __init__(self, rt):
        self.root = rt
        self.questions = load_questions()  # Загружаем все вопросы
        self.current_index = 0  # Индекс текущего вопроса
        self.current_frame = None  # Фрейм для текущего вопроса

        # Создаем постоянные элементы
        self.create_header_row()
        self.create_question_frame()
        self.create_answer_button_row()

        # Отображаем первый вопрос
        self.show_current_question()

    def create_header_row(self):
        """Создает информативную строку с заголовками"""
        header = Label(root, text="Задание", font=("Arial", 12, "bold"),
                        bg="lightgray", padx=10, pady=5)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=1, pady=1)

    def create_question_frame(self):
        """Создает фрейм для вопроса (он будет переиспользоваться)"""
        self.question_frame = Frame(self.root, bg="white", relief="sunken", bd=1)
        self.question_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def create_answer_button_row(self):
        """Создает кнопку проверки"""
        button_frame = Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.check_button = Button(button_frame, text="Проверить ответ",
                                   command=self.check_answer,
                                   font=("Arial", 12), bg="green", fg="white")
        self.check_button.pack()

        # Добавим метку для отображения результата
        self.result_label = Label(button_frame, text="", font=("Arial", 11))
        self.result_label.pack(pady=5)

    def create_choices_row(self, q: Question):
        """Создает строку с вариантами ответов и галочками"""
        question_label = Label(self.question_frame,
                               text=q.question_text,
                               font=("Arial", 11), bg="white")
        question_label.pack(anchor="w", padx=5, pady=2)

        # Фрейм для вариантов
        choices_frame = Frame(self.question_frame, bg="white")
        choices_frame.pack(anchor="w", padx=20, pady=5)

        # Создаем варианты с галочками (Checkbutton)
        self.check_variants = []
        choice_count = len(q.variants)
        for i in range(choice_count):
            self.check_variants.append(BooleanVar())
            (Checkbutton(choices_frame, text=q.variants[i],
                         variable=self.check_variants[i], bg="white")
             .grid(row=i, column=0, padx=10, sticky="w"))

    def create_text_gap_row(self, q: Question):
        """Создает строку с текстом и пропуском для ввода"""
        # Создаем текст с пропуском
        Label(self.question_frame, text="Вставьте пропущенное слово:",
              font=("Arial", 11), bg="white").pack(anchor="w", padx=5, pady=2)

        # Текст вопроса
        Label(self.question_frame, text=q.question_text,
              bg="white").pack(anchor="w", padx=20)

        # Поле для ввода пропущенного слова
        self.text_answer = Entry(self.question_frame, width=15, font=("Arial", 11))
        self.text_answer.pack(anchor="w", padx=20, pady=(5, 10))

    def show_current_question(self):
        """Отображает текущий вопрос"""
        # Очищаем фрейм вопроса
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        if self.current_index < len(self.questions):
            question = self.questions[self.current_index]

            # Отображаем номер вопроса
            Label(self.question_frame,
                  text=f"Вопрос {self.current_index + 1} из {len(self.questions)}",
                  font=("Arial", 10, "italic"), bg="white").pack(anchor="w", padx=5, pady=2)

            # Отображаем сам вопрос в зависимости от типа
            if not question.is_text:
                self.create_choices_row(question)
            else:
                self.create_text_gap_row(question)
        else:
            # Все вопросы закончились
            Label(self.question_frame, text="Викторина завершена!",
                  font=("Arial", 14, "bold"), bg="white").pack(pady=20)
            self.check_button.config(state="disabled")

    def check_answer(self):
        """Проверяет ответ и переходит к следующему вопросу"""
        if self.current_index >= len(self.questions):
            return

        question = self.questions[self.current_index]
        user_answer = None

        # Получаем ответ пользователя в зависимости от типа вопроса
        if not question.is_text:
            user_answer = []
            for i, val in enumerate(self.check_variants):
                user_answer.append(self.check_variants[i].get())
        else:
            user_answer = self.text_answer.get().strip()

        print(user_answer)
        # Проверяем правильность (здесь ваша логика проверки)
        is_correct = self.is_answer_correct(question, user_answer)

        # Показываем результат
        if is_correct:
            self.result_label.config(text="✅ Правильно!", fg="green")
        elif not is_correct and question.is_text:
            self.result_label.config(text=f"❌ Неправильно. Правильный ответ: {question.text_answer}",
                                     fg="red")
        else:
            self.result_label.config(text=f"❌ Неправильно. Правильный ответ: {question.right_variants}",
                                     fg="red")

        # Переходим к следующему вопросу через небольшую задержку
        self.root.after(2000, self.next_question)

    def next_question(self):
        """Переходит к следующему вопросу"""
        self.current_index += 1
        self.result_label.config(text="")  # Очищаем результат
        self.show_current_question()

    def is_answer_correct(self, question, user_answer):
        """Проверяет правильность ответа (реализуйте свою логику)"""
        if not question.is_text:
            return user_answer == question.right_variants
        else:
            return user_answer.lower() == question.text_answer.lower()

root = Tk()
root.title("Examinator11")
root.geometry("500x500")
app = QuizApp(root)
root.mainloop()