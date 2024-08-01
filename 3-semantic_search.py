import os
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout

WEAVIATE_CLUSTER_URL = os.getenv('WEAVIATE_CLUSTER_URL')
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_CLUSTER_URL,
    auth_credentials=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
    headers={"X-OpenAI-Api-Key": OPENAI_API_KEY})

try:
    print(client.is_connected())

    book_collection = client.collections.get(name="Book")

    # Semantic Search
    response = book_collection.query.near_text(

        # Prompt the user for query and limit
        query = input("What type of books are you looking for? "),
        limit = int(input("Limit the amount of books being recommended(choose any number): "))

    )

    print()
    for book in response.objects:
            print(f"Title: {book.properties['title']}")
            print(f"Published Year: {book.properties['published_year']}")
            print(f"Authors: {book.properties['authors']}")
            print(f"Rating: {book.properties['average_rating']}")
            print('---')

finally:
    # Ensure the client is closed properly
    client.close() 