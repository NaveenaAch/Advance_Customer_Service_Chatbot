def chunk_document(document, chunk_size=200, overlap=100):
    """
    Split a document into smaller chunks of specified size with overlap.

    Args:
    - document (str): The text to be chunked.
    - chunk_size (int): The number of words per chunk.
    - overlap (int): The number of overlapping words between consecutive chunks.

    Returns:
    - List[str]: List of text chunks.
    """
    words = document.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks
