import chromadb
import uuid

client = chromadb.Client()


def store_embeddings(embeddings, metadata, chunks):
    """
    Function to store embeddings in ChromaDB.

    Args:
    - embeddings (list of list): List of embedding vectors.
    - metadata (list of dict): List of metadata dictionaries corresponding to each embedding.
    """

    try:
        collection = client.get_collection("my_collection")
    except chromadb.errors.InvalidCollectionException:
        # Create the collection if it does not exist
        collection = client.create_collection("my_collection")






    # Ensure embeddings are a list of lists of floats or ints
    if not all(isinstance(embedding, list) and all(isinstance(x, (float, int)) for x in embedding) for embedding in
               embeddings):
        raise ValueError("All embeddings must be a list of lists of floats or ints.")

    # Generate unique IDs for each embedding
    ids = [str(uuid.uuid4()) for _ in embeddings]

    # Add embeddings with their corresponding metadata and IDs
    collection.add(ids=ids,               # Unique IDs for each chunk
    embeddings=embeddings, # Embedding vectors
    metadatas=metadata,    # Metadata (source and chunk index)
    documents=chunks)



def retrieve_similar_documents(query_embedding, top_k=5):


    try:
            collection = client.get_collection("my_collection")

    except chromadb.errors.InvalidCollectionException:
            raise ValueError(
                "Collection 'my_collection' does not exist. Please ensure it is created and populated before querying.")

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)


    if 'metadatas' in results and len(results['metadatas']) > 0:
        documents = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            documents.append({
                'document': doc,
                'metadata': metadata
            })
        return documents
    else:
        print(f"Unexpected response structure: {results}")
        return []






