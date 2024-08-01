# ta_wv
Weaviate Demonstration

In this demonstration, I will set up a Weaviate cloud instance for EcomMax. The instance will be populated with a dataset using the Python client v4 and some code available within this repository. This setup aims to showcase the benefits of the managed Weaviate cloud platform, including semantic and generative search integrated with the OpenAI API.

The demo is inspired by the ideas in the following GitHub repository, with credits to the original creators: https://github.com/weaviate/BookRecs

While setting up the demo environment, I encountered slow import times for the majority of the books. To address this, I implemented a parallelized import to expedite the data importing process. Although batch importing is also possible, I chose the parallelized approach for this demo.

This demonstration will be accompanied by a presentation, which is available here: https://docs.google.com/presentation/d/1ERWEGL5y4HEhnjOdSAM0wrhrAjGs8uYPkj1Tig7Zxwk/edit?usp=sharing


###
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install weaviate-client 
 
###
python3 1-create_collection.py

###
curl --request GET \
  --url https://wv/v1/schema \
  --header "Authorization: Bearer $WEAVIATE_API_KEY" | jq

###
python3 2-populate.py

###
curl -X GET "https://wv/v1/objects?class=Book&limit=600" \
     -H "Authorization: Bearer $WEAVIATE_API_KEY" \
     -H "Content-Type: application/json" | jq

###
python3 3-semantic_search.py

###
pip install python-dotenv

###
python3 4-generative_search.py
