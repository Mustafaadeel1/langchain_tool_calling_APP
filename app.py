import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from tools import (text_to_speech, speech_to_text, image_to_text, Calculator, 
                    fetch_latest_news, get_random_joke, fetch_stock_data)
from langchain.tools import Tool


# Example tool definitions
tools = {
    "Image to Text": Tool(
        name="image_to_text",
        func=image_to_text,  # Replace with your actual function
        description="Extracts text from images."
    ),    

    "News Fetcher": Tool(
        name="news_fetcher",
        func=fetch_latest_news,  # Replace with your actual function
        description="Fetches the latest news based on the input topic."
    ),
    "Stock Data Fetcher": Tool(
        name="stock_data_fetcher",
        func=fetch_stock_data,  # Replace with your actual function
        description="Retrieves stock market data for the given stock ticker."
    ),
    "Speech to Text": Tool(
        name="speech_to_text",
        func=speech_to_text,  # Replace with your actual function
        description="Converts spoken words to text."
    ),
    "Text to Speech": Tool(
        name="text_to_speech",
        func=text_to_speech,  # Replace with your actual function
        description="Converts text to speech audio."
    ),
    "Joke Generator": Tool(
        name="joke_generator",
        func=get_random_joke,  # Replace with your actual function
        description="Generates a random joke to lighten the mood."
    ),
    "Calculator": Tool(
        name="calculator",
        func=Calculator,  # Replace with your actual function
        description="Performs basic arithmetic operations."
    )
}

tools_list = list(tools.values())  # Extract the tool objects (functions or identifiers)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    api_key="AIzaSyCipxZmb0iHDi9vukeeKbb77xSVxvFheZs",  # Replace with your actual API key
)

# Pass the tools_list instead of tools
agent = initialize_agent(
    tools_list, 
    llm, 
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
)


# Streamlit Page Configuration
st.set_page_config(
    page_title="Langchain Tools Calling Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Add Custom CSS for Styling
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput > div > input {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        border: 2px solid #444444;
        border-radius: 5px;
        background-color: #2e2e2e;
        color: #ffffff;
    }
    .stButton > button {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        background-color: #007bff;
        color: black;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .tool-names {
        font-size: 18px;
        color: #00ffff;
        margin-bottom: 15px;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #aaaaaa;
        margin-top: 30px;
    }
    .sidebar-title {
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for Tool Selection
# Replace with your list of tools
tools = {
    "Text Summarizer": "summarizer_tool",
    "News Fetcher": "news_fetch_tool",
    "Stock Data Retriever": "stock_tool",
    "AI Chatbot": "chatbot_tool",
    "Calculator": "calculator_tool",
    "Text to Speech": "text_to_speech",
    "Joke Generator": "joke_generator",
}


tool_names = list(tools.keys())  # Extract all tool names dynamically

# Sidebar for Tool Selection
st.sidebar.title("🛠️ Tools")
selected_tool_name = st.sidebar.radio("Choose a Tool:", tool_names)
selected_tool = tools[selected_tool_name]

# App Title and Description
st.title("🤖 Langchain Tools Calling Agent")
st.markdown(
    """
    Welcome to the **Langchain Tools Calling Agent**! 
    Unlock the power of conversational AI by leveraging advanced tools like APIs, models, and more.
    """
)

# Input Section
placeholder_text = f"Type something for {selected_tool_name}..."
st.subheader("🔍 Input Section")
user_input = st.text_input(
    label="Enter your prompt below:",
    placeholder=placeholder_text,
    help="Provide a query to process with the selected tool.",
)

# Submit Button and Response Section
if st.button("🚀 Submit Query", key="submit_button"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a valid prompt before submitting.")
    else:
        try:
            with st.spinner(f"Processing with {selected_tool_name}..."):
                response = agent.run(user_input)
            st.success("🎉 Agent's Response:")
            st.write(response)

            # Text-to-Speech Option
            if st.button("🔊 Play Response", key="play_response_button"):
                tts_message = text_to_speech(response)
                st.info(tts_message)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Footer Section
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <strong>About:</strong> This app leverages **Langchain** to integrate conversational AI with tools like news APIs, stock data fetchers, 
        and advanced text generation models. Built with ❤️ using [Streamlit](https://streamlit.io/).
    </div>
    """,
    unsafe_allow_html=True,
)

