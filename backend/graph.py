from langgraph.graph import StateGraph, END
from .state import PitchState
from .deconstructor import narrative_deconstructor
from .refiner import prompt_refiner
from .generator import image_generator

def create_pitch_graph():
    builder = StateGraph(PitchState)
    
    # Add Nodes
    builder.add_node("deconstruct", narrative_deconstructor)
    builder.add_node("refine", prompt_refiner)
    builder.add_node("generate", image_generator)
    
    # Set Edges
    builder.set_entry_point("deconstruct")
    builder.add_edge("deconstruct", "refine")
    builder.add_edge("refine", "generate")
    builder.add_edge("generate", END)
    
    return builder.compile()

pitch_graph = create_pitch_graph()
