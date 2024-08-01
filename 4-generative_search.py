import os
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout

from dotenv import load_dotenv

load_dotenv()

WEAVIATE_CLUSTER_URL = os.getenv('WEAVIATE_CLUSTER_URL')
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_CLUSTER_URL,
    auth_credentials=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
    headers={"X-OpenAI-Api-Key": OPENAI_API_KEY})

try:
    # Check connection
    if client.is_connected():
        print("Welcome to EcomMax Books, your ultimate destination for everything literature. Dive into a world of endless stories and boundless knowledge, where every page brings a new adventure. Your literary journey begins here.")
    
        # Fetch the book collection
        book_collection = client.collections.get(name="Book")

        

        # Generative Search
        response = book_collection.generate.near_text(
            query = input("What type of book are you looking for?: "),
            limit = int(input("Search result limit ")),
            single_prompt = "Summarize why this book titled '{title}', described as '{description}', in the '{categories}' genre, might interest someone."
        )
        

        # Print the results
        print("\nSearch Results:\n")
        for book in response.objects:
            print(f"Title: {book.properties['title']}\n")
            print("Generated Text:")
            print(book.generated)  # Print the generated text for each book
            print("\n" + "-"*40 + "\n")

    else:
        print("Failed to connect to Weaviate Cloud")
finally:
    # Ensure the client is closed properly
    client.close()