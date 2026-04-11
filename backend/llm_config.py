import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Global Model Configuration (Lazy Loaded)
_LLM = None

def get_llm():
    global _LLM
    if _LLM is None:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key or "your_groq_api_key_here" in groq_api_key:
            print("WARNING: GROQ_API_KEY not set or invalid in .env ", flush=True)
            
        print("Establishing connection to Groq Cloud (Llama 3.3 70B) ", flush=True)
        chat_model = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=groq_api_key
        )
        _LLM = chat_model | StrOutputParser()
    return _LLM
