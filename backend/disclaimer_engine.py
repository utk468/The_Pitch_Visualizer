from .state import TriageState

def disclaimer_engine(state: TriageState):
    print("DISCLAIMER ENGINE")
    disclaimer = "\n\n DISCLAIMER: This assistant is for informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. If you think you may have a medical emergency, call your doctor or 911 immediately."
    return {"final_response": state["final_response"] + disclaimer}
