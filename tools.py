from langchain_core.tools import tool 
import math
import requests
from PIL import Image
import pyttsx3
import random
import speech_recognition as sr
import speech_recognition as sr
import speech_recognition as sr
from PIL import Image
import pytesseract
# Tool 1: Text to Speech

@tool
def text_to_speech(text: str):
    """
    Converts the input text to speech using the pyttsx3 library.

    Args:
        text (str): The input text to be converted to speech.

    Returns:
        str: A message indicating whether the speech synthesis was successful or not.
    """
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "Speech synthesis complete."
    except Exception as e:
        return {"error": str(e)}

#import speech_recognition as sr
import speech_recognition as sr

@tool
def speech_to_text():
    """
    Converts speech to text using Google Speech Recognition.

    Returns:
        str: The transcribed text from speech, or an error message in case of failure.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            return text
        except Exception as e:
            return {"error": str(e)}


@tool
def image_to_text(image_path: str) -> str:
    """
    Extracts text from an image using Tesseract OCR.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text from the image.
    """
    try:
        # Open the image file
        img = Image.open(image_path)

        # Use Tesseract to perform OCR on the image
        extracted_text = pytesseract.image_to_string(img)

        return extracted_text.strip()  # Remove any extra whitespace
    except FileNotFoundError:
        return "❌ Error: The specified image file was not found."
    except Exception as e:
        return f"❌ Error: {str(e)}"
# Tool 4: Calculator
@tool
def Calculator(expression):
    """
    Evaluates a mathematical expression with custom support for functions like SUM and AVG.

    Args:
        expression (str): A mathematical expression starting with '='.

    Returns:
        str or float: The result of the evaluation or an error message if the syntax is incorrect.
    """
    if not expression.startswith('='):
        return "Error: Expression must start with '='."

    expression = expression[1:].strip()

    def SUM(*args):
        """Calculates the sum of provided numbers."""
        return sum(args)

    def AVG(*args):
        """Calculates the average of provided numbers."""
        return sum(args) / len(args) if args else 0

    allowed_functions = {
        'SUM': SUM,
        'AVG': AVG,
        **{k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    }

    try:
        result = eval(expression, {"__builtins__": None}, allowed_functions)
    except Exception as e:
        return f"Error in evaluation: {e}"

    return result

# Tool 5: Fetch Latest News
@tool
def fetch_latest_news(category='general', country='us'):
    """
    Retrieves the latest news articles from NewsAPI.

    Args:
        category (str): The category of news to fetch (default: 'general').
        country (str): The country code to filter news by location (default: 'us').

    Returns:
        str: A formatted string of the latest news headlines or an error message if fetching fails.
    """
    api_key = '39245a2fc2e24025a7644b5c6c1e2cc2'
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country={country}&apiKey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if articles:
                news = [f"{i+1}. {article['title']} (Source: {article['source']['name']})" 
                        for i, article in enumerate(articles[:5])]
                return "\n".join(news)
            else:
                return "No news articles found."
        else:
            return f"Error: Unable to fetch news (Status Code: {response.status_code})"
    except Exception as e:
        return {"error": str(e)}

# Tool 6: Get Random Joke
from langchain.tools import StructuredTool

@tool
def get_random_joke():
    """
    Provides a random joke from a predefined list in English, Urdu, and Punjabi.

    Returns:
        str: A randomly selected joke.
    """

    jokes = [
        # English jokes
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An impasta.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        
        # Urdu jokes
        "ایک آدمی ڈاکٹر کے پاس گیا، کہا: ڈاکٹر صاحب میں بہت تھکا ہوا ہوں۔ ڈاکٹر نے کہا: تو آرام کر لو، وہ آدمی بولا: ڈاکٹر صاحب مجھے سکون دو، آرام تو خود ہی کر رہا ہوں!",
        "میرے دوست نے کہا: تمھاری آنکھوں میں چمک ہے، میں نے کہا: شکر ہے، نظر تو نہیں آرہی!",
        
        # Punjabi jokes
        "پہلا بندہ: 'ہمارے پاس بہت دلچسپ باتیں ہیں!' دوسرا بندہ: 'کیا ہیں؟' پہلا بندہ: 'تو بھی سوچ، اور میں بھی سوچ!'",
        "بچہ اپنے پیرے سے: 'بابا، آپ آج کہاں گئے تھے؟' پیرے نے کہا: 'جدھر اور تو؟' بچہ: 'وہ کھانا چھوڑ کے تو بھی ادھر آ، تمہیں نہیں جانا!'",
    ]
    try:
        return random.choice(jokes)
    except Exception as e:
        return f"Error occurred: {str(e)}"

@tool
def fetch_stock_data(ticker):
    """
    Fetch stock data for the given ticker symbol using Alpha Vantage.

    Args:
    - ticker (str): The stock ticker symbol (e.g., 'AAPL', 'GOOGL').

    Returns:
    - str: Stock information or an error message.
    """
    import requests

    api_key = "AqWbGjogZ8vS2XDCQjo3X3A3495ouUGb"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if "Global Quote" in data:
            quote = data["Global Quote"]
            return (
                f"Stock: {ticker.upper()}\n"
                f"Current Price: ${quote.get('05. price', 'N/A')}\n"
                f"Previous Close: ${quote.get('08. previous close', 'N/A')}\n"
                f"Day's High: ${quote.get('03. high', 'N/A')}\n"
                f"Day's Low: ${quote.get('04. low', 'N/A')}\n"
                f"Volume: {quote.get('06. volume', 'N/A')}\n"
            )
        else:
            return "Error: No stock data found for the given ticker."
    except Exception as e:
        return f"Error fetching stock data: {e}"
