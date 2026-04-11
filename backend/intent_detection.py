from .state import TriageState
from .llm_config import get_llm

def intent_detection(state: TriageState):
    print("INTENT DETECTION")
    prompt = f"Categorize the following medical query into 'symptom', 'general', or 'diet'. Query: {state['query']}. Respond only with the category name."
    intent = get_llm().invoke(prompt).strip().lower()
    return {"intent": intent}
