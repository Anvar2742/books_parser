import csv
import os
import requests
import re

# Функция для загрузки изображения
def download_image(url, save_folder, file_name):
    try:
        # Проверяем, существует ли папка, и создаем, если нет
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        file_path = os.path.join(save_folder, file_name)

        # Загружаем изображение
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Сохраняем изображение
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Изображение сохранено: {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return False

# Функция для чтения данных из CSV
def get_books_from_csv(file_path, image_column, title_column):
    books = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if image_column in row and title_column in row:
                    image_url = row[image_column].strip()
                    title = row[title_column].strip()
                    books.append((image_url, title))
        return books
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        return []

# Функция для создания безопасного имени файла
def sanitize_filename(name):
    # Удаляем или заменяем недопустимые символы
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

# Путь к CSV-файлу
csv_file_path = "books.csv"

# Имена столбцов
image_column = "image_url"
title_column = "title"

# Папка для сохранения изображений
save_folder = "downloaded_images"

# Получаем список ссылок и названий книг
books = get_books_from_csv(csv_file_path, image_column, title_column)

# Скачиваем все изображения
for i, (url, title) in enumerate(books, start=1):
    # Создаем безопасное имя файла из названия книги
    file_name = f"{sanitize_filename(title)}.jpg"
    if url:  # Проверяем, что URL не пустой
        download_image(url, save_folder, file_name)
