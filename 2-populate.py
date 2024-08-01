import os
import csv
import weaviate
import weaviate.classes as wvc

WEAVIATE_CLUSTER_URL = os.getenv('WEAVIATE_CLUSTER_URL')
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_CLUSTER_URL,
    auth_credentials=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
    headers={"X-OpenAI-Api-Key": OPENAI_API_KEY})

book_collection = client.collections.get(name="Book")

f = open("7k-books-kaggle.csv", "r")
current_book = None
try:
    reader = csv.reader(f)
    # Iterate through each row of data
    for book in reader:
      current_book = book
      # 0 - isbn13
      # 1 - isbn10
      # 2 - title
      # 3 - subtitle
      # 4 - authors
      # 5 - categories
      # 6 - thumbnail
      # 7 - description
      # 8 - published_year
      # 9 - average_rating
      # 10 - num_pages
      # 11 - ratings_count

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

      print(f"{book[2]}: {uuid}", end='\n')
except Exception as e:
  print(f"Exception: {e}.")

f.close()
client.close()