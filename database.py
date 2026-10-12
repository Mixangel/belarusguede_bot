import sqlite3

def init_db():
    conn = sqlite3.connect('belarus_project.db')
    cursor = conn.cursor()

    # Таблица для справочных материалов (история, достопримечательности, культура)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS references_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # Таблица для вопросов викторины (проверка знаний)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            correct_option INTEGER NOT NULL
        )
    ''')

    # Заполняем справочник стартовыми данными
    cursor.execute("SELECT COUNT(*) FROM references_info")
    if cursor.fetchone()[0] == 0:
        sample_refs = [
            ("Брестская крепость", "Героический мемориал, принявший первый удар немецко-фашистских захватчиков 22 июня 1941 года."),
            ("Беловежская пуща", "Один из старейших заповедников Европы, где обитает популяция зубров. Внесена в список Всемирного наследия ЮНЕСКО."),
            ("Государственные символы РБ", "Государственный флаг, герб и гимн являются официальными символами суверенитета Республики Беларусь.")
        ]
        cursor.executemany("INSERT INTO references_info (title, description) VALUES (?, ?)", sample_refs)

    # Заполняем вопросы для викторины
    cursor.execute("SELECT COUNT(*) FROM quiz")
    if cursor.fetchone()[0] == 0:
        sample_quiz = [
            ("В каком году началась Великая Отечественная война?", "1939", "1941", "1945", 2),
            ("Какой заповедник является самым известным в Беларуси?", "Беловежская пуща", "Припятский", "Нарочанский", 1),
            ("Какая столица у Республики Беларусь?", "Гродно", "Минск", "Брест", 2)
        ]
        cursor.executemany("INSERT INTO quiz (question, option1, option2, option3, correct_option) VALUES (?, ?, ?, ?, ?)", sample_quiz)

    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена!")

if __name__ == '__main__':
    init_db()