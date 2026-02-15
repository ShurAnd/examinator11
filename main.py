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
    button_frame: Frame
    answer_button: Button
    check_button: Button
    result_label: Label
    text_answer: Entry
    check_variants: list[BooleanVar]
    nav_entry: Entry

    def __init__(self, rt):
        self.root = rt
        self.questions = load_questions()  # Загружаем все вопросы
        self.current_index = 0  # Индекс текущего вопроса
        self.current_frame = None  # Фрейм для текущего вопроса

        # Создаем постоянные элементы
        self.create_header_row()
        self.create_navigation_frame()
        self.create_question_frame()
        self.create_answer_button_row()

        # Настраиваем веса для главного окна
        self.root.grid_rowconfigure(2, weight=1)  # Строка с вопросом растягивается (сдвинулась на row=2)
        self.root.grid_rowconfigure(0, weight=0)  # Заголовок не растягивается
        self.root.grid_rowconfigure(1, weight=0)  # Навигация не растягивается
        self.root.grid_rowconfigure(3, weight=0)  # Кнопки не растягиваются
        self.root.grid_columnconfigure(0, weight=1)  # Растягиваем по ширине

        # Отображаем первый вопрос
        self.show_current_question()

    def create_header_row(self):
        """Создает информативную строку с заголовками"""
        header = Label(root, text="Задание", font=("Arial", 12, "bold"),
                        bg="lightgray", padx=10, pady=5)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=1, pady=1)

    def create_navigation_frame(self):
        """Создает фрейм для навигации по вопросам"""
        nav_frame = Frame(self.root, bg="lightblue", padx=10, pady=5)
        nav_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Настраиваем веса для навигационного фрейма
        nav_frame.grid_columnconfigure(1, weight=1)  # Растягиваем среднюю колонку

        # Метка
        Label(nav_frame, text="Перейти к вопросу №:",
                bg="lightblue", font=("Arial", 10)).grid(row=0, column=0, padx=5)

        # Поле для ввода (максимум 3 цифры)
        self.nav_entry = Entry(nav_frame, width=5, font=("Arial", 10), justify="center")
        self.nav_entry.grid(row=0, column=1, padx=5, sticky="w")

        # Кнопка "Начать"
        start_button = Button(nav_frame, text="Начать",
                                command=self.jump_to_question,
                                font=("Arial", 10), bg="green", fg="white")
        start_button.grid(row=0, column=2, padx=5)

    def jump_to_question(self):
        """Переходит к указанному номеру вопроса"""
        try:
            # Получаем значение из поля ввода
            question_num = int(self.nav_entry.get())

            # Проверяем, что номер в допустимом диапазоне (от 1 до количества вопросов)
            if 1 <= question_num <= len(self.questions):
                # Переходим к указанному вопросу (индекс = номер - 1)
                self.current_index = question_num - 1

                # Очищаем фрейм вопроса
                for widget in self.question_frame.winfo_children():
                    widget.destroy()

                # Сбрасываем результат
                self.result_label.config(text="")

                # Обновляем кнопку на "Проверить ответ", если нужно
                if hasattr(self, 'check_button') and self.check_button.winfo_exists():
                    self.check_button.destroy()
                self.check_button = Button(self.button_frame, text="Проверить ответ",
                                           command=self.check_answer,
                                           font=("Arial", 12), bg="green", fg="white")
                self.check_button.pack()

                # Отображаем выбранный вопрос
                self.show_current_question()

                # Очищаем поле ввода
                self.nav_entry.delete(0, END)
            else:
                # Показываем сообщение об ошибке в результате
                self.result_label.config(text=f"Введите число от 1 до {len(self.questions)}", fg="orange")
        except ValueError:
            # Если поле пустое или введено не число
            if self.nav_entry.get().strip() == "":
                self.result_label.config(text="Введите номер вопроса", fg="orange")
            else:
                self.result_label.config(text="Введите корректное число", fg="orange")

    def create_question_frame(self):
        """Создает фрейм для вопроса (он будет переиспользоваться)"""
        self.question_frame = Frame(self.root, bg="white", relief="sunken", bd=1)
        self.question_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Настраиваем веса внутри фрейма вопроса
        self.question_frame.grid_rowconfigure(0, weight=0)  # Заголовок с номером вопроса
        self.question_frame.grid_rowconfigure(1, weight=0)  # Текст вопроса
        self.question_frame.grid_rowconfigure(2, weight=1)  # Контент (варианты/поле ввода) растягивается
        self.question_frame.grid_columnconfigure(0, weight=1)  # Растягиваем по ширине

    def create_answer_button_row(self):
        """Создает кнопку проверки"""
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.check_button = Button(self.button_frame, text="Проверить ответ",
                                   command=self.check_answer,
                                   font=("Arial", 12), bg="green", fg="white")
        self.check_button.pack()

        # Добавим метку для отображения результата
        self.result_label = Label(self.button_frame, text="", font=("Arial", 11))
        self.result_label.pack(pady=5)

    def create_choices_row(self, q: Question):
        """Создает строку с вариантами ответов и галочками"""
        # Создаем фрейм для контента, который будет растягиваться
        content_frame = Frame(self.question_frame, bg="white")
        content_frame.grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)  # Растягиваем по ширине
        content_frame.grid_rowconfigure(0, weight=1)  # Растягиваем по высоте

        # Текст вопроса (помещаем в отдельную строку)
        question_label = Label(self.question_frame,
                               text=q.question_text,
                               font=("Arial", 11), bg="white")
        question_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        # Фрейм для вариантов (внутри content_frame)
        choices_frame = Frame(content_frame, bg="white")
        choices_frame.pack(expand=True, fill="both", anchor="center")  # Центрируем и растягиваем

        # Создаем варианты с галочками (Checkbutton)
        self.check_variants = []
        choice_count = len(q.variants)

        # Центрируем варианты по вертикали
        choices_frame.grid_rowconfigure(0, weight=1)  # Отступ сверху
        choices_frame.grid_rowconfigure(choice_count + 1, weight=1)  # Отступ снизу

        for i in range(choice_count):
            self.check_variants.append(BooleanVar())
            cb = Checkbutton(choices_frame, text=q.variants[i],
                             variable=self.check_variants[i], bg="white")
            cb.grid(row=i + 1, column=0, padx=10, pady=2, sticky="w")  # Выравниваем по левому краю

        # Центрируем колонку с вариантами
        choices_frame.grid_columnconfigure(0, weight=1)  # Растягиваем по ширине

    def create_text_gap_row(self, q: Question):
        """Создает строку с текстом и пропуском для ввода"""
        # Создаем фрейм для контента, который будет растягиваться
        content_frame = Frame(self.question_frame, bg="white")
        content_frame.grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)  # Растягиваем по ширине
        content_frame.grid_rowconfigure(0, weight=1)  # Растягиваем по высоте
        content_frame.grid_rowconfigure(1, weight=0)  # Для текста
        content_frame.grid_rowconfigure(2, weight=0)  # Для поля ввода
        content_frame.grid_rowconfigure(3, weight=1)  # Отступ снизу

        # Текст с пропуском
        Label(self.question_frame, text="Вставьте пропущенное слово:",
              font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=2)

        # Текст вопроса
        Label(content_frame, text=q.question_text,
              bg="white").grid(row=1, column=0, sticky="w", padx=20)

        # Поле для ввода пропущенного слова
        self.text_answer = Entry(content_frame, width=15, font=("Arial", 11))
        self.text_answer.grid(row=2, column=0, sticky="w", padx=20, pady=(5, 10))

    def show_current_question(self):
        """Отображает текущий вопрос"""
        # Очищаем фрейм
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        if self.current_index < len(self.questions):
            question = self.questions[self.current_index]

            # Отображаем номер вопроса в первой строке
            Label(self.question_frame,
                  text=f"Вопрос {self.current_index + 1} из {len(self.questions)}",
                  font=("Arial", 10, "italic"), bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=2)

            # Отображаем сам вопрос в зависимости от типа
            if not question.is_text:
                self.create_choices_row(question)
            else:
                self.create_text_gap_row(question)
        else:
            # Все вопросы закончились - центрируем сообщение
            self.question_frame.grid_rowconfigure(0, weight=1)
            self.question_frame.grid_columnconfigure(0, weight=1)

            Label(self.question_frame, text="Тест завершен!",
                  font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0)

            self.check_button.destroy()
            self.check_button = Button(self.button_frame, text="Следующий вопрос",
                                       command=self.check_answer,
                                       font=("Arial", 12), bg="green", fg="white")
            self.check_button.pack()
            self.check_button.config(state=DISABLED)


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
        self.check_button.destroy()
        self.check_button = Button(self.button_frame, text="Следующий вопрос",
                                   command=self.next_question,
                                   font=("Arial", 12), bg="green", fg="white")
        self.check_button.pack()

    def next_question(self):
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        self.check_button.destroy()
        self.check_button = Button(self.button_frame, text="Проверить ответ",
                                   command=self.check_answer,
                                   font=("Arial", 12), bg="green", fg="white")
        self.check_button.pack()
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