from email.utils import parsedate_to_datetime

import openai
import json
import os

# Set up OpenAI API key
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
api_key = os.getenv("API_KEY")

def translate_to_english(text):
    """
    Translates text to English and returns a structured dictionary.
    """
    try:
        messages = [
            {"role": "system", "content": "You are a translator. Return translations in JSON format."},
            {"role": "user", "content": f"Translate this  text to English:\n\n{text}\n\n"
                                        "Output format (JSON): {{'original_text': '...', 'translated_text': '...','source_language':'...'}}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=1000
        )

        # Extract and parse the JSON response from GPT
        raw_output = response.choices[0].message['content'].strip()
        print(raw_output)
        parsed_translation = json.loads(raw_output)  # Convert string to dict
        print(parsed_translation)
        return parsed_translation

    except json.JSONDecodeError:
        return {"error": "Translation response was not valid JSON"}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}


def translate_from_english(text,target_language):
    # Use a valid chat model ID and the v1/chat/completions endpoint
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Translate the following text from english to {target_language}  \n\n{text}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Ensure this model ID is correct and supported
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()
