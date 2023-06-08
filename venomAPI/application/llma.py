from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import os

import os.path
os.environ['OPENAI_API_KEY'] = "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"

documents = SimpleDirectoryReader('data').load_data()
print(documents)
index = GPTVectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)