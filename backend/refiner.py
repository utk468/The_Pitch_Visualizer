import os
from groq import Groq
from .state import PitchState

def prompt_refiner(state: PitchState):
    """
    Node to enhance each scene segment into a detailed visual prompt using Groq.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    segments = state["segments"]
    style = state.get("style", "digital art")
    
    prompts = []
    
    for segment in segments:
        instr = f"""
        Convert this scene into a detailed AI image prompt. 
        Style: {style}
        Scene: {segment}
        Output only the prompt paragraph.
        """
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert AI prompt engineer."},
                    {"role": "user", "content": instr}
                ],
                model="llama-3.3-70b-versatile"
            )
            prompts.append(response.choices[0].message.content.strip())
        except Exception as e:
            print(f"Refiner Error: {e}")
            prompts.append(f"{segment}, {style}")
            
    return {"prompts": prompts}
