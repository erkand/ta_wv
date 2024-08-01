import os
import csv
import weaviate
from weaviate.auth import AuthApiKey
from concurrent.futures import ThreadPoolExecutor, as_completed

WEAVIATE_CLUSTER_URL = os.getenv('WEAVIATE_CLUSTER_URL')
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_CLUSTER_URL,
    auth_credentials=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
    headers={"X-OpenAI-Api-Key": OPENAI_API_KEY})

book_collection = client.collections.get(name="Book")

def read_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row if there is one
        for row in reader:
            yield row

def insert_book(book):
    properties = {
        "isbn13": book[0],
        "isbn10": book[1],
        "title": book[2],
        "subtitle": book[3],
        "authors": book[4],
        "categories": book[5],
        "thumbnail": book[6],
        "description": book[7],
        "published_year": book[8],
        "average_rating": book[9],
        "num_pages": book[10],
        "ratings_count": book[11],
    }

    uuid = book_collection.data.insert(properties)      
    print(f"{book[2]}: {uuid}")

def insert_books_in_parallel(file_path, max_workers=5):
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(insert_book, book) for book in read_csv(file_path)]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    insert_books_in_parallel("7k-books-kaggle.csv")