from .state import TriageState

def input_processor(state: TriageState):
    print("INPUT PROCESSOR")
    return {"query": state["query"].strip()}
