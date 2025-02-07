
import openai
import requests
from load_pdf import load_pdf
from load_markdown import load_markdown
from chunk_documents import chunk_document
from embed_text import get_embedding
from store_embeddings import store_embeddings
from response_generation import generate_response, create_prompt
from translation import translate_to_english, translate_from_english
from store_embeddings import retrieve_similar_documents
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
api_key = os.getenv("API_KEY")
openai.api_key = api_key

def initialize_system():
    """Initialize the system by loading and processing documents once."""
# Load documents
documents = []
# Define the paths of y our PDF and Markdown files
pdf_files = [
    r'C:/Users/Asus/OneDrive/Documents/Frequently Asked Questions.pdf',
    r'C:/Users/Asus/OneDrive/Documents/ReceiveMoney.pdf',
    r'C:/Users/Asus/Downloads/valid_qa_pairs (1).pdf',
    r'C:/Users/Asus/Downloads/How_to_Send_Money_CITY_EXPRESS_FIXED.pdf'
]

md_files = [
    'D:/new_folder/service_fee.md',
    'D:/new_folder/westernunion.md'
]

# Load PDF files
for pdf_file in pdf_files:
    text = load_pdf(pdf_file)
    documents.append((text, pdf_file))

# Load Markdown files
for md_file in md_files:
    text = load_markdown(md_file)
    documents.append((text, md_file))

# Chunk documents
all_chunks = []
for text, source in documents:
    chunks = chunk_document(text)
    all_chunks.extend(chunks)

# Prepare metadata for each chunk
all_metadata = []
for text, source in documents:
    chunks = chunk_document(text)
    all_metadata.extend([{'source': source, 'chunk_index': i} for i in range(len(chunks))])

# Get embeddings for all chunks
all_embeddings = [get_embedding(chunk) for chunk in all_chunks]

# Store embeddings in ChromaDB
store_embeddings(all_embeddings, all_metadata, all_chunks)
print("System initialized successfully.")

print("All embeddings have been stored successfully.")

def handle_query(query):


    # Step 1: Translate to English
    print("Translating query to English...")
    translation_result = translate_to_english(query)
    query_in_english = translation_result['translated_text']
    source_language = translation_result['source_language']
    print(f"Query in English: {query_in_english}")
    print(f"Source language: {source_language}")


    # Step 2: Generate the query embedding
    print("Generating query embedding...")
    query_embedding = get_embedding(query_in_english)
    # print(f"Query embedding: {query_embedding}")

    # Step 3: Perform vector search in ChromaDB
    print("Retrieving similar documents from ChromaDB...")
    similar_documents = retrieve_similar_documents(query_embedding, top_k=5)
    print(f"Similar documents: {similar_documents}")

    # Step 4: Construct the prompt for response generation
    context = "\n".join([doc['document'] for doc in similar_documents])
    prompt = create_prompt(context, query_in_english)
    # print(f"Constructed prompt: {prompt}")

    # Step 5: Generate the response
    print("Generating response...")
    response_in_english = generate_response(prompt)
    print(f"Response in English: {response_in_english}")

    # return response_in_english

    # Step 6: Translate the response back to the target language
    print("Translating response to target language...")
    response_in_target_language = translate_from_english(response_in_english,source_language)
    print(f"{response_in_target_language}")

    # Return the final response
    return {
        "translated_text": response_in_target_language,
        "source_language": source_language
    }

# #

if __name__ == "__main__":
    # user_query = ("お金を送るにはどうすればいいですか？")
    # Replace the hardcoded value with input
    user_query = input("Enter your query: ")

    # Print the query to confirm
    print(f"You entered: {user_query}")

    # final_response = handle_query(user_query, source_lang)
    final_response = handle_query(user_query)
    print("Response:", final_response)



















