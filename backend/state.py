from typing import TypedDict, List

class TriageState(TypedDict):
    query: str
    intent: str
    symptoms: List[str]
    risk_level: str
    final_response: str
    history: List[str]
