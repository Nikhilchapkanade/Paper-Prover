import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()

# --- VISION BRAIN (Gemini 1.5 Pro) ---
# Used for "seeing" charts and complex reasoning
llm_vision = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- SPEED BRAIN (Llama 3.3 via Groq) ---
# UPDATED: Swapped "llama3-70b-8192" (Retired) for "llama-3.3-70b-versatile" (Newest)
llm_fast = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# --- DATABASE CONFIG ---
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))