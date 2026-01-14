from typing import TypedDict, List

class AgentState(TypedDict):
    paper_content: str
    vision_data: str
    debate_history: List[str]
    critique_count: int