from langgraph.graph import StateGraph, END
from backend.state import TriageState
from backend.input_processor import input_processor
from backend.intent_detection import intent_detection
from backend.symptom_analysis import symptom_analysis
from backend.risk_detection import risk_detection
from backend.llm_generator import llm_generator
from backend.safety_filter import safety_filter
from backend.disclaimer_engine import disclaimer_engine

builder = StateGraph(TriageState)
builder.add_node("process_input", input_processor)
builder.add_node("detect_intent", intent_detection)
builder.add_node("analyze_symptoms", symptom_analysis)
builder.add_node("detect_risk", risk_detection)
builder.add_node("generate_response", llm_generator)
builder.add_node("apply_safety", safety_filter)
builder.add_node("add_disclaimer", disclaimer_engine)

builder.set_entry_point("process_input")
builder.add_edge("process_input", "detect_intent")
builder.add_edge("detect_intent", "analyze_symptoms")
builder.add_edge("analyze_symptoms", "detect_risk")
builder.add_edge("detect_risk", "generate_response")
builder.add_edge("generate_response", "apply_safety")
builder.add_edge("apply_safety", "add_disclaimer")
builder.add_edge("add_disclaimer", END)

triage_graph = builder.compile()
