import markdown

def load_markdown(file_path: str) -> str:
    """
    Function to load and convert a Markdown file to plain text.
    
    Args:
    - file_path (str): Path to the Markdown file.

    Returns:
    - str: Converted plain text from the Markdown file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return markdown.markdown(text)