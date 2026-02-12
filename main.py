from tkinter import *
from tkinter import ttk

class question:
    def __init__(self, identifier: int,
                 is_text: bool,
                 text_answer: str,
                 var_count: int,
                 variants: list[str],
                 right_variant: int):
        self.identifier = identifier
        self.variants = variants
        self.right_variant = right_variant

def prev_card():
    print("prev")

def next_card():
    print("next")

root = Tk()
root.title("Examinator11")
root.geometry("500x300")

# Настройка весов для столбцов
root.grid_columnconfigure(0, weight=1)  # Первый столбец + второй (объединенный)
root.grid_columnconfigure(1, weight=0)  # Второй столбец (не используется отдельно)
root.grid_columnconfigure(2, weight=0)  # Третий столбец (фиксированный)

def create_header_row():
    """Создает информативную строку с заголовками"""
    header1 = Label(root, text="Задание", font=("Arial", 12, "bold"),
                       bg="lightgray", padx=10, pady=5)
    header1.grid(row=0, column=0, columnspan=2, sticky="ew", padx=1, pady=1)

    header3 = Label(root, text="Ответ", font=("Arial", 12, "bold"),
                       bg="lightgray", padx=10, pady=5)
    header3.grid(row=0, column=2, sticky="ew", padx=1, pady=1)


def create_choices_row():
    """Создает строку с вариантами ответов и галочками"""
    # Фрейм для текста с вариантами (объединенные столбцы 1 и 2)
    text_frame = Frame(root, bg="white", relief="sunken", bd=1)
    text_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    # Текст с вариантами
    question_label = Label(text_frame,
                              text="Выберите правильный ответ:",
                              font=("Arial", 11), bg="white")
    question_label.pack(anchor="w", padx=5, pady=2)

    # Фрейм для вариантов
    choices_frame = Frame(text_frame, bg="white")
    choices_frame.pack(anchor="w", padx=20, pady=5)

    # Создаем варианты с галочками (Checkbutton)
    choice_var1 = BooleanVar()
    choice_var2 = BooleanVar()
    choice_var3 = BooleanVar()

    choice1 = Checkbutton(choices_frame, text="Вариант 1",
                             variable=choice_var1, bg="white")
    choice1.grid(row=0, column=0, padx=10, sticky="w")

    choice2 = Checkbutton(choices_frame, text="Вариант 2",
                             variable=choice_var2, bg="white")
    choice2.grid(row=0, column=1, padx=10, sticky="w")

    choice3 = Checkbutton(choices_frame, text="Вариант 3",
                             variable=choice_var3, bg="white")
    choice3.grid(row=0, column=2, padx=10, sticky="w")

    # В третьем столбце - галочка для отметки правильного ответа
    answer_frame = Frame(root, bg="lightyellow", relief="raised", bd=1)
    answer_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

    Label(answer_frame, text="Правильный ответ:",
             bg="lightyellow").pack(pady=5)

    correct_answer_var = BooleanVar()
    correct_check = Checkbutton(answer_frame, text="Отметить",
                                   variable=correct_answer_var,
                                   bg="lightyellow")
    correct_check.pack(pady=5)


def create_text_gap_row():
    """Создает строку с текстом и пропуском для ввода"""
    # Фрейм для текста с пропуском (объединенные столбцы 1 и 2)
    text_frame = Frame(root, bg="white", relief="sunken", bd=1)
    text_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    # Создаем текст с пропуском
    Label(text_frame, text="Вставьте пропущенное слово:",
             font=("Arial", 11), bg="white").pack(anchor="w", padx=5, pady=2)

    gap_frame = Frame(text_frame, bg="white")
    gap_frame.pack(anchor="w", padx=20, pady=10)

    # Часть текста до пропуска
    Label(gap_frame, text="Москва — столица ",
             bg="white").pack(side="left")

    # Поле для ввода пропущенного слова
    gap_entry = Entry(gap_frame, width=15, font=("Arial", 11))
    gap_entry.pack(side="left", padx=5)
    gap_entry.insert(0, "введите слово")

    # Часть текста после пропуска
    Label(gap_frame, text=".", bg="white").pack(side="left")

    # В третьем столбце - дополнительное поле или информация
    info_frame = Frame(root, bg="lightblue", relief="raised", bd=1)
    info_frame.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    Label(info_frame, text="Ваш ответ:",
             bg="lightblue").pack(pady=5)

    # Отображаем введенный текст (можно связать с Entry)
    answer_display = Label(info_frame, text="",
                                   bg="white", width=15, height=2,
                                   relief="sunken")
    answer_display.pack(pady=5, padx=5)

    # Кнопка для проверки/отображения ответа
    Button(info_frame, text="Проверить",
              command=check_answer(gap_entry, answer_display)).pack(pady=5)


def check_answer(gap_entry: Entry, answer_display: Label):
    """Проверяет введенный ответ"""
    answer = gap_entry.get()
    answer_display.config(text=f"Ответ: {answer}")


def add_custom_row(self, row_num, question_text, answer_type="choices"):
    """
    Метод для добавления новых строк с разными типами заданий
    """
    if answer_type == "choices":
        # Создаем строку с вариантами ответов
        pass
    elif answer_type == "gap":
        pass

# Первая строка - информативная
create_header_row()

# Вторая строка - пример с вариантами ответов (галочки)
create_choices_row()

# Третья строка - пример с пропуском текста (поле ввода)
create_text_gap_row()

root.mainloop()