from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.prompts import RESEARCHER_PROMPT, SKEPTIC_PROMPT
from config import llm_fast

def researcher_node(state: AgentState):
    prompt = f"{RESEARCHER_PROMPT}\n\nTEXT: {state['paper_content'][:2000]}\nDATA: {state['vision_data']}"
    response = llm_fast.invoke(prompt)
    new_history = state["debate_history"] + [f"🕵️ RESEARCHER: {response.content}"]
    return {"debate_history": new_history}

def skeptic_node(state: AgentState):
    last_point = state["debate_history"][-1]
    prompt = f"{SKEPTIC_PROMPT}\n\nCLAIM: {last_point}"
    response = llm_fast.invoke(prompt)
    new_history = state["debate_history"] + [f"⚖️ SKEPTIC: {response.content}"]
    return {
        "debate_history": new_history, 
        "critique_count": state["critique_count"] + 1
    }

def judge_logic(state: AgentState):
    if state["critique_count"] >= 2:
        return "end"
    return "continue"

workflow = StateGraph(AgentState)
workflow.add_node("Researcher", researcher_node)
workflow.add_node("Skeptic", skeptic_node)
workflow.set_entry_point("Researcher")
workflow.add_edge("Researcher", "Skeptic")
workflow.add_conditional_edges("Skeptic", judge_logic, {"continue": "Researcher", "end": END})

app_swarm = workflow.compile()