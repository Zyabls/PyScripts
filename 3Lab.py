import sqlite3
import requests

# Функция для создания базы данных и таблицы
def create_database():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    # Создаем таблицу posts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Функция для очистки таблицы
def clear_table():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM posts')
    
    conn.commit()
    conn.close()

# Функция для получения данных с тестового сервера
def fetch_data():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка при получении данных: {response.status_code}")

# Функция для сохранения данных в базу данных
def save_data_to_db(posts):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    for post in posts:
        cursor.execute('''
            INSERT INTO posts (id, user_id, title, body)
            VALUES (?, ?, ?, ?)
        ''', (post['id'], post['userId'], post['title'], post['body']))
    
    conn.commit()
    conn.close()

# Функция для чтения данных из базы данных
def read_data_from_db(user_id):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()
    
    conn.close()
    return posts

def main():
    # Создание базы данных и таблицы
    create_database()
    
    # Очистка таблицы перед вставкой новых данных
    clear_table()
    
    # Получение данных с сервера
    posts = fetch_data()
    
    # Сохранение данных в базу данных
    save_data_to_db(posts)
    
    # Чтение данных из базы данных
    user_id = 1  # Пример user_id для выборки
    user_posts = read_data_from_db(user_id)
    for post in user_posts:
        print(post)

if __name__ == "__main__":
    main()