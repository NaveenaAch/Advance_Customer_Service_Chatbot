import streamlit as st
from main import handle_query, initialize_system
from PIL import Image
import base64
import time


def get_base64_image(image_path):
    """Converts an image file to a Base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def initialize_chat_interface():
    st.set_page_config(
        page_title="Multilingual Chat Assistant",
        page_icon="💬",
        layout="centered"
    )
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "system_initialized" not in st.session_state:
        st.session_state.system_initialized = False


def display_response(response):
    if isinstance(response, dict) and 'translated_text' in response:
        return f"{response['translated_text']}"
    return "Response in target language: [Error: Invalid response format]"


def main():
    initialize_chat_interface()

    # Convert image to Base64
    icon_path = r"D:/New folder (1)/project/CityExpressIcon.png"
    company_icon_base64 = get_base64_image(icon_path)

    # Display header with inline Base64 image
    st.markdown(f'''
        <style>
        .header-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }}
        .company-logo {{
            max-width: 60px;
            height: auto;
            margin-bottom: 8px;
        }}
        .header-text {{
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
        }}
        .info-text {{
            font-size: 18px;
            color: #dcdcdc;
        }}
        </style>
        <div class="header-container">
            <img class="company-logo" src="data:image/png;base64,{company_icon_base64}" />
            <div class="header-text">CITY EXPRESS CUSTOMER SERVICE ASSISTANCE</div>
            <div class="info-text">I'm here to help you with:</div>
            <ul class="info-text">
                <li>Information about City Express services</li>
                <li>General inquiries related to Remittance</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)

    # Initialize the system if not done yet
    if not st.session_state.system_initialized:
        with st.spinner("Initializing system... This may take a few moments."):
            initialize_system()
            st.session_state.system_initialized = True
            st.success("System initialized successfully!")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                try:
                    response = handle_query(prompt)
                    formatted_response = display_response(response)
                    message_placeholder.markdown(formatted_response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": formatted_response
                    })
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    message_placeholder.markdown("Response in target language: [Error: Could not process the request]")

    # Sidebar Information
    with st.sidebar:
        st.title("About")
        st.markdown("""
        This chat assistant can:
        - Answer questions in multiple languages
        - Provide information about money transfers
        - Help with common queries about services
        """)
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
