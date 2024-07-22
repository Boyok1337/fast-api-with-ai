import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

HARM_PROBABILITY = ["LOW", "MEDIUM", "HIGH"]

genai.configure(api_key=os.environ["google_ai_api_key"])

MODEL = genai.GenerativeModel("gemini-1.5-flash")
