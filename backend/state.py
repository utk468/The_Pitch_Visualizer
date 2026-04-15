from typing import TypedDict, List, Dict, Any

class PitchState(TypedDict):
    """
    State for the Pitch Visualizer Graph.
    """
    narrative: str
    style: str
    segments: List[str]
    prompts: List[str]
    image_urls: List[str]
    storyboard: List[Dict[str, Any]]
    error: str
