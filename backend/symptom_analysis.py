from .state import TriageState
from .llm_config import get_llm

def symptom_analysis(state: TriageState):
    print("SYMPTOM ANALYSIS")
    if state["intent"] != "symptom":
        return {"symptoms": []}
    prompt = f"Extract symptoms from this query: {state['query']}. Return ONLY a comma-separated list of identified symptoms. NO other text. Respond with 'none' if no symptoms found."
    symptoms_text = get_llm().invoke(prompt).strip()
    symptoms = [s.strip() for s in symptoms_text.split(",") if s.strip() != "none"]
    return {"symptoms": symptoms}
