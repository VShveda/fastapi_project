import os

from dotenv import load_dotenv
from google import generativeai

load_dotenv()

API_KEY = os.getenv("API_KEY")
generativeai.configure(api_key=API_KEY)


def is_toxic_content(text: str) -> bool:
    prompt = f"""
        Analyze the following message and determine if it contains toxic content:
        "{text}"
    
        If the content is toxic, return True. If it is not, return False.
        """

    try:
        model = generativeai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        message = response.text.lower()

        return "true" in message
    except Exception as e:
        print(f"Error analyzing content: {e}")
        return False
