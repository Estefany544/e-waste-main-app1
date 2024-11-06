# config.py
import os
from turtle import st
# Try to load environment variables, but don't fail if .env file is missing
try:
    from dotenv import load_dotenv # type: ignore
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Using default API key.")

# Use environment variable i available, otherwise use a default value
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_default_api_key_here")

def get_variable(name):
    if hasattr(st, 'secrets') and name in st.secrets:
        return st.secrets[name]

GROQ_API_KEY = get_variable('GROQ_API_KEY')
REPLICATE_API_TOKEN = get_variable('REPLICATE_API_TOKEN')
HG_API_KEY = get_variable('HG_API_KEY')
