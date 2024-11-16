import requests

# 1. GET-запрос: Запросить список постов и вывести те, которые принадлежат пользователям с чётным ID.
def get_even_user_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    
    if response.status_code == 200:
        posts = response.json()
        print("Посты пользователей с чётными ID:")
        for post in posts:
            if post['userId'] % 2 == 0:
                print(post)
    else:
        print(f"Ошибка при выполнении GET-запроса: {response.status_code}")

# 2. POST-запрос: Создать новый пост и вывести JSON-ответ.
def create_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    new_post = {
        "title": "Тестовый пост",
        "body": "Это тело тестового поста",
        "userId": 1
    }
    
    response = requests.post(url, json=new_post)
    
    if response.status_code == 201:
        print("Создан новый пост:")
        print(response.json())
        return response.json()  # Возвращаем JSON для дальнейшего использования
    else:
        print(f"Ошибка при создании поста: {response.status_code}")
        return None

# 3. PUT-запрос: Обновить ранее созданный пост.
def update_post(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    updated_post = {
        "title": "Обновлённый пост",
        "body": "Это обновлённое тело поста",
        "userId": 1
    }
    
    response = requests.put(url, json=updated_post)
    
    if response.status_code == 200:
        print("Пост обновлён:")
        print(response.json())
    else:
        print(f"Ошибка при обновлении поста: {response.status_code}")

def main():
    # Выполнение GET-запроса
    get_even_user_posts()
    
    # Выполнение POST-запроса и получение ID нового поста
    new_post = create_post()
    if new_post:
        post_id = new_post['id']
        
        # Выполнение PUT-запроса для обновления созданного поста
        update_post(post_id)

if __name__ == "__main__":
    main()
