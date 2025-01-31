
import openai
def generate_response(prompt):
    # Use a valid chat model and the v1/chat/completions endpoint
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Ensure this model ID is correct and supported
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()
def create_prompt(context, user_query):
    prompt = f"""
    You are an AI-powered chatbot designed to answer user queries based on provided context. Your task is to analyze the given context and formulate a relevant, accurate, and helpful response to the user's query.

    Here is the context information:
    <context>
    {context}
    </context>

    And here is the user's query:
    <query>
    {user_query}
    </query>

    Please follow these steps to formulate your response:

    1. Carefully read and analyze the provided context.
    2. Identify the key information in the context that is relevant to the user's query.
    3. Formulate a clear and concise answer based on the relevant information from the context.
    4. Ensure that your answer directly addresses the user's query.
    5. If the context provides multiple relevant pieces of information, synthesize them into a coherent response.
    6. Use a friendly and helpful tone in your response.
    7. Ensure to include any URLs or links provided in the context instead of placeholder texts.
    8. In response, provide  link of website of related user_query if avilable.
    Format your response as follows:
    <answer>
    Your response here
    </answer>

    If the user's query cannot be fully answered based on the provided context, or if the query is unclear or out of scope, respond as follows:
    <answer>
    I apologize, but I don't have enough information in my current context to fully answer your question about [brief mention of the query topic]. Is there a more specific aspect of this topic you'd like to know about, or would you like me to provide general information based on what I have available?
    </answer>

    Remember, do not include any information that is not supported by the given context. If you need to make any assumptions or inferences, clearly state them as such in your response.

    Now, please provide your response to the user's query based on the given context.
    """
    return prompt


if __name__ == "__main__":
    result = """
    Frequently Asked Questions - City Express-Japan
    Q1. How can I register as a member to use the remittance service?
    A: To register, please visit the following link: https://cityexpress.jp/register
    """
    user_query = "how can i register through mobile app?"
    prompt = create_prompt(result, user_query)
    response = generate_response(prompt)

    # print("Response:", response)