import tkinter as tk
from tkinter import messagebox, simpledialog, END
import random
import json
import os

QUOTES_DATABASE = [
    {"text": "Жизнь — это то, что происходит, пока ты строишь другие планы.", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Работа"},
    {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "topic": "Образование"},
    {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "topic": "Успех"},
]

history = []  
FILE_NAME = 'quotes_history.json'

def generate_quote():
    """Выбирает случайную цитату из базы и добавляет её в историю."""
    if not QUOTES_DATABASE:
        messagebox.showwarning("База пуста", "В базе данных нет цитат.")
        return
    quote = random.choice(QUOTES_DATABASE)
    quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')
    history.append(quote)
    update_history_list()

def update_history_list():
    """Обновляет виджет списка истории."""
    history_listbox.delete(0, END)
    for q in history:
        history_listbox.insert(END, f'"{q["text"]}" — {q["author"]}')

def save_history():
    """Сохраняет историю в JSON файл."""
    try:
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", f"История сохранена в {FILE_NAME}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

def load_history():
    """Загружает историю из JSON файла."""
    global history
    if not os.path.exists(FILE_NAME):
        messagebox.showwarning("Файл не найден", f"Файл {FILE_NAME} не существует.")
        return
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            history = json.load(f)
        update_history_list()
        messagebox.showinfo("Успех", f"История загружена из {FILE_NAME}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

def filter_history():
    """Фильтрует историю по автору и/или теме."""
    author = author_entry.get().strip().lower()
    topic = topic_entry.get().strip().lower()
    
    history_listbox.delete(0, END)
    
    for q in history:
        match_author = (author == "") or (author in q["author"].lower())
        match_topic = (topic == "") or (topic in q["topic"].lower())
        
        if match_author and match_topic:
            history_listbox.insert(END, f'"{q["text"]}" — {q["author"]}')

def add_quote():
    """Добавляет новую цитату в базу данных с проверкой на пустые строки."""
    text = simpledialog.askstring("Добавить цитату", "Введите текст цитаты:")
    
    if not text or text.strip() == "":
        messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым.")
        return

    author = simpledialog.askstring("Добавить цитату", "Введите автора:")
    
    if not author or author.strip() == "":
        messagebox.showerror("Ошибка", "Имя автора не может быть пустым.")
        return

    topic = simpledialog.askstring("Добавить цитату", "Введите тему:")
    
    if not topic or topic.strip() == "":
        messagebox.showerror("Ошибка", "Тема не может быть пустой.")
        return

    new_quote = {"text": text.strip(), "author": author.strip(), "topic": topic.strip()}
    QUOTES_DATABASE.append(new_quote)
    messagebox.showinfo("Успех", "Цитата добавлена в базу данных!")

root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x500")
root.resizable(False, False)

quote_frame = tk.LabelFrame(root, text="Случайная цитата", padx=10, pady=10)
quote_frame.pack(padx=10, pady=10, fill="x")

quote_label = tk.Label(quote_frame, text="Нажмите кнопку для генерации цитаты", wraplength=400, justify="center")
quote_label.pack()

btn_generate = tk.Button(quote_frame, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(pady=5)

history_frame = tk.LabelFrame(root, text="История и фильтры", padx=10, pady=10)
history_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

filter_frame = tk.Frame(history_frame)
filter_frame.pack(fill="x")

tk.Label(filter_frame, text="Автор:").pack(side="left")
author_entry = tk.Entry(filter_frame)
author_entry.pack(side="left", fill="x", expand=True, padx=(0,5))

tk.Label(filter_frame, text="Тема:").pack(side="left")
topic_entry = tk.Entry(filter_frame)
topic_entry.pack(side="left", fill="x", expand=True, padx=(0,5))

btn_filter = tk.Button(filter_frame, text="Фильтровать", command=filter_history)
btn_filter.pack(side="left")

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side="right", fill="y")

history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=10)
history_listbox.pack(side="left", fill="both", expand=True)
scrollbar.config(command=history_listbox.yview)

control_frame = tk.Frame(root)
control_frame.pack(pady=5)

btn_save = tk.Button(control_frame, text="Сохранить историю (JSON)", command=save_history)
btn_save.pack(side="left", padx=5)

btn_load = tk.Button(control_frame, text="Загрузить историю (JSON)", command=load_history)
btn_load.pack(side="left", padx=5)

btn_add = tk.Button(control_frame, text="Добавить цитату в базу", command=add_quote)
btn_add.pack(side="left", padx=5)

root.mainloop()