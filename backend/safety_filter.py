from .state import TriageState
from .llm_config import get_llm

def safety_filter(state: TriageState):
    print("SAFETY FILTER")
    # Rule: Never prescribe medicine or diagnose specifically.
    prompt = (
        f"You are a medical safety compliance officer. "
        f"Your task is to refine the following response for safety while PRESERVING ALL DETAILED CLINICAL EXPLANATIONS AND STRUCTURE. "
        f"1. Remove ONLY definitive diagnosis claims (e.g., change 'You have X' to 'The symptoms are consistent with X'). "
        f"2. Remove ONLY specific medicine prescriptions (e.g., instead of 'Take 500mg X', say 'Consider OTC options like X if suitable'). "
        f"3. DO NOT remove the 'Possible Causes', 'What to Avoid', or 'What to Do' sections. "
        f"4. DO NOT make the response vague or generic. Keep the specific reasoning. "
        f"Respond ONLY with the refined text. No introductory chatter. "
        f"Response to refine: {state['final_response']}"
    )
    filtered = get_llm().invoke(prompt)
    return {"final_response": filtered}
