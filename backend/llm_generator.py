from .state import TriageState
from .llm_config import get_llm

def llm_generator(state: TriageState):
    print(f"LLM GENERATOR (Risk: {state['risk_level']})")
    risk = state["risk_level"]
    
    structure_instruction = (
        "Strictly adhere to the following 3-section structure for your response:\n"
        "1. **Possible Causes**: Provide specific, clinical context for what might be happening (e.g., mention allergies, infections, or inflammatory responses). Do NOT use vague phrases like 'various factors' or 'several causes'. Be as detailed as a triage expert would be.\n"
        "2. **What to Avoid**: List specific triggers, foods, medications, or activities that could worsen the situation based on the symptoms.\n"
        "3. **What to Do**: Provide clear, actionable self-care steps, non-prescription management, and specific 'red flags' that require immediate medical attention.\n"
    )

    expertise_instruction = (
        "You are an expert medical triage assistant with deep clinical knowledge. "
        "Your goal is to be helpful and specific. Avoid filler text. "
        "Explain the 'why' behind the symptoms using medical terminology appropriately."
    )

    prompt = (
        f"Query: {state['query']}\n"
        f"Risk Level: {risk}\n\n"
        f"{expertise_instruction}\n\n"
        f"{structure_instruction}\n\n"
        f"IF RISK IS 'EMERGENCY', prioritize life-saving advice but STILL follow the 3 sections. "
        f"Generate an expert response based on your vast clinical knowledge database."
    )
        
    response = get_llm().invoke(prompt)
    return {"final_response": response}
