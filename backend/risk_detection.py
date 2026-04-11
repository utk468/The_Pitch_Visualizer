from .state import TriageState
from .llm_config import get_llm

def risk_detection(state: TriageState):
    print("RISK DETECTION")
    if state["intent"] != "symptom":
        return {"risk_level": "Normal"}
    prompt = f"Assess the risk level (Normal, Moderate, Emergency) for these symptoms: {', '.join(state['symptoms'])}. If chest pain, sudden numbness, or severe bleeding is present, it's 'Emergency'. Respond only with the risk level."
    risk = get_llm().invoke(prompt).strip()
    return {"risk_level": risk}
