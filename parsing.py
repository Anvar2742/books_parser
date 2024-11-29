import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# Base URL for the book catalog
base_url = "https://librarius.md/ru/catalog/tops"

# Load genre translations from file
def load_genre_translations(file_path):
    genre_translation = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            exec(f.read(), {}, genre_translation)  # Load the genre_translation dictionary
        return genre_translation['genre_translation']
    except Exception as e:
        print(f"Error loading genre translations: {e}")
        return {}

# Function to collect links to books
def collect_book_links(base_url, max_books=10):
    book_links = []
    page = 1
    while len(book_links) < max_books:  # Collect until we have max_books links
        print(f"Collecting links from page {page}...")
        try:
            response = requests.get(f"{base_url}?page={page}")
            response.raise_for_status()  # Check response status
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all divs with class 'anyproduct-card'
            divs = soup.find_all('div', class_='anyproduct-card')
            for div in divs:
                if len(book_links) >= max_books:  # Stop if we reach the limit
                    break
                # Find <a> tag inside each div
                link = div.find('a', href=True)
                if link:
                    href = link['href']
                    if href.startswith('/ru'):  # Relative link
                        book_links.append(f"https://librarius.md{href}")
                    elif href.startswith('http'):  # Absolute link
                        book_links.append(href)
        except requests.RequestException as e:
            print(f"Error loading catalog page {page}: {e}")
        page += 1  # Move to the next page
        time.sleep(random.uniform(0.5, 1.5))  # Random delay
    print(f"Total links found: {len(book_links)}")
    return book_links[:max_books]  # Return exactly max_books links

# Function to parse book genres
def extract_genre(attributes, genre_translation):
    genre = attributes.get("Жанр", None)
    return genre_translation.get(genre, genre)  # Replace with translation if available

# Function to parse data from a book page
def parse_book_page(book_url, genre_translation):
    try:
        response = requests.get(book_url)
        response.raise_for_status()  # Check response status
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract book title
        title_tag = soup.find('h1', class_='main-title')
        title = title_tag.text.strip() if title_tag else 'Not specified'

        # Extract price
        price_tag = soup.find('div', class_='product-book-price__actual')
        price = None
        if price_tag:
            price = next((text.strip() for text in price_tag.contents if isinstance(text, str)), 'Not specified')

        # Extract stock status
        stock_label = soup.find('span', class_='stock-label')
        stock = stock_label.text.strip() if stock_label else 'Not specified'

        # Extract image URL
        image_tag = soup.find('img', class_='wp-post-image')
        image_url = f"{image_tag['src']}" if image_tag else 'Image not available'

        # Extract description (only text content)
        description_tag = soup.find('div', class_='book-page-description')
        description = description_tag.get_text(strip=True).replace('\n', ' ') if description_tag else 'Description not available'

        # Extract attributes
        attributes = parse_book_attributes(soup)

        # Extract genre and translate
        genre = extract_genre(attributes, genre_translation)

        return {
            'title': title,
            'price': price,
            'stock': stock,
            'image_url': image_url,
            'description': description,
            'attributes': attributes,
            'genre': genre,
            'url': book_url
        }
    except Exception as e:
        print(f"Error parsing page {book_url}: {e}")
        return None

# Function to extract attributes
def parse_book_attributes(soup):
    attributes = {}
    props_box = soup.find('div', class_='product-page-props-box')
    if props_box:
        rows = props_box.find_all('div', class_='row book-props-item')
        for row in rows:
            name_tag = row.find('div', class_='book-prop-name')
            value_tag = row.find('div', class_='book-prop-value')
            if name_tag and value_tag:
                name = name_tag.text.strip()
                value = value_tag.text.strip()
                attributes[name] = value
    return attributes

# Main process
def main():
    # Load genre translations from file
    genre_translation = load_genre_translations('genres.txt')

    # Collect links to books
    book_links = collect_book_links(base_url, max_books=100)  # Adjust max_books as needed

    # Parse data for each book
    book_data = []
    for i, book_url in enumerate(book_links, start=1):
        print(f"Parsing book {i}/{len(book_links)}: {book_url}")
        book_info = parse_book_page(book_url, genre_translation)
        if book_info:
            book_data.append(book_info)
        time.sleep(random.uniform(0.5, 1.5))  # Random delay

    # Save data to CSV
    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'price', 'stock', 'image_url', 'description', 'genre', 'url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for book in book_data:
            row = {key: book.get(key, '') for key in fieldnames}
            writer.writerow(row)

    print("Data successfully saved to books.csv")

# Run the script
if __name__ == "__main__":
    main()
