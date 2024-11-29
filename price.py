import csv
import math

# Конвертация лей в евро (примерный курс)
LEI_TO_EURO = 0.05  # Замените на актуальный курс
MARKUP_PERCENT = 30  # Наценка в процентах

# Функция для расчета цены в евро с наценкой и увеличением цены
def convert_price_to_euro(price_in_lei, conversion_rate, markup_percent):
    try:
        # Удаляем все нечисловые символы, например, пробелы, запятые
        price = float(price_in_lei.replace(',', '').replace(' ', ''))
        price_in_euro = price * conversion_rate
        final_price = price_in_euro * (1 + markup_percent / 100) + 1  # Наценка + фиксированная прибавка
        # Округляем вверх до ближайшего целого числа, затем добавляем 0.99
        rounded_price = math.ceil(final_price) + 0.99
        return round(rounded_price, 2)  # Возвращаем результат с двумя знаками после запятой
    except ValueError as e:
        print(f"Ошибка преобразования цены '{price_in_lei}': {e}")
        return None  # Если не удается преобразовать цену

# Путь к файлу
csv_file_path = "books.csv"
updated_csv_file_path = "books_updated.csv"

# Чтение и обновление цен
def update_prices_in_csv(input_file, output_file, price_column):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            if price_column not in fieldnames:
                print(f"Колонка '{price_column}' не найдена в CSV.")
                return
            
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                original_price = row.get(price_column, "").strip()
                if original_price:
                    converted_price = convert_price_to_euro(original_price, LEI_TO_EURO, MARKUP_PERCENT)
                    if converted_price is not None:
                        row[price_column] = converted_price  # Обновляем цену
                        print(f"Цена обновлена: {original_price} лей → {converted_price} евро")
                    else:
                        print(f"Цена не обновлена: {original_price}")
                writer.writerow(row)

        print(f"Цены успешно обновлены. Результат сохранен в '{output_file}'.")
    except Exception as e:
        print(f"Ошибка: {e}")

# Имя столбца с ценами
price_column = "price"

# Запуск процесса обновления цен
update_prices_in_csv(csv_file_path, updated_csv_file_path, price_column)
