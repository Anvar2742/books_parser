import csv

# Конвертация лей в евро (примерный курс)
LEI_TO_EURO = 0.05

# Функция для перевода лей в евро
def convert_lei_to_euro(price_in_lei):
    try:
        price = float(price_in_lei.replace(',', '').replace(' ', ''))  # Удаляем пробелы и запятые
        return round(price * LEI_TO_EURO, 2)  # Округляем до двух знаков
    except ValueError:
        return None

# Функция для чтения цен из CSV
def read_prices_from_csv(file_path, price_column, key_column="title"):
    prices = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row.get(key_column, "").strip()
                price = row.get(price_column, "").strip()
                if title and price:
                    prices[title] = price
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
    return prices

# Путь к файлам
books_csv_path = "books.csv"
books_updated_csv_path = "books_updated.csv"

# Чтение данных из обоих файлов
books_prices_lei = read_prices_from_csv(books_csv_path, price_column="price", key_column="title")
books_prices_euro = read_prices_from_csv(books_updated_csv_path, price_column="price", key_column="title")

# Сравнение цен
comparison_results = []
for title, price_lei in books_prices_lei.items():
    converted_price = convert_lei_to_euro(price_lei)
    updated_price = float(books_prices_euro.get(title, 0))  # Цена в евро из updated файла

    if converted_price is not None:
        adjusted_price = updated_price - 2  # Отнимаем 2 евро от обновленной цены
        difference = round(adjusted_price - converted_price, 2)  # Разница между ценами
        difference_percentage = round((difference / converted_price) * 100, 2) if converted_price != 0 else 0

        comparison_results.append({
            "title": title,
            "price_in_lei": price_lei,
            "converted_price_in_euro": converted_price,
            "updated_price_in_euro": updated_price,
            "adjusted_price_in_euro": adjusted_price,
            "difference": difference,
            "difference_percentage": difference_percentage,
        })

# Вывод результатов
print(f"{'Название книги':<50}{'Цена в лей':<15}{'Переведенная цена (евро)':<25}{'Обновленная цена (евро)':<25}{'Цена -2 евро':<15}{'Разница':<10}{'Разница (%)':<15}")
for result in comparison_results:
    print(f"{result['title']:<50}{result['price_in_lei']:<15}{result['converted_price_in_euro']:<25}{result['updated_price_in_euro']:<25}{result['adjusted_price_in_euro']:<15}{result['difference']:<10}{result['difference_percentage']:<15}")

# Сохранение в CSV
output_file = "price_comparison_adjusted.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ["title", "price_in_lei", "converted_price_in_euro", "updated_price_in_euro", "adjusted_price_in_euro", "difference", "difference_percentage"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(comparison_results)

print(f"Результаты сохранены в {output_file}")
