import os
import json
from groq import Groq
from .state import PitchState

def narrative_deconstructor(state: PitchState):
    """
    Node to segment narrative text into logical storyboard scenes using Groq.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    text = state["narrative"]
    
    prompt = f"""
    Break down the following narrative into exactly 3-5 logical scenes for a storyboard.
    Return only a JSON list of strings.
    
    Narrative: {text}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a storyboard artist. Output valid JSON list of strings only."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        content = json.loads(response.choices[0].message.content)
        # Handle different potential JSON structures
        if isinstance(content, list):
            segments = content
        elif isinstance(content, dict):
            segments = next(iter(content.values())) if isinstance(next(iter(content.values())), list) else [str(v) for v in content.values()]
        else:
            segments = [s.strip() for s in text.split('.') if s.strip()][:5]
            
        return {"segments": segments}
    except Exception as e:
        print(f"Deconstructor Error: {e}")
        return {"segments": [s.strip() for s in text.split('.') if s.strip()][:5], "error": str(e)}
