from langgraph.graph import StateGraph
from typing import TypedDict

# -------------------------
# STATE DEFINITION
# -------------------------
class State(TypedDict):
    input: str
    output: dict


# -------------------------
# TOOLS (5 tools)
# -------------------------
def log_interaction(state: State):
    return {
        "output": {
            "tool": "log_interaction",
            "result": f"Logged interaction: {state['input']}"
        }
    }


def suggest_next_step(state: State):
    return {
        "output": {
            "tool": "suggest_next_step",
            "result": "Next step: Follow up with the doctor."
        }
    }


def fetch_patient_info(state: State):
    return {
        "output": {
            "tool": "fetch_patient_info",
            "result": f"Fetched patient details for: {state['input']}"
        }
    }


def send_notification(state: State):
    return {
        "output": {
            "tool": "send_notification",
            "result": f"Notification sent for: {state['input']}"
        }
    }


def summarize(state: State):
    return {
        "output": {
            "tool": "summarize",
            "result": f"Summary: {state['input'][:50]}..."
        }
    }


# -------------------------
# DECISION / ROUTER
# -------------------------
def route_tool(state: State):
    text = state["input"].lower()

    if "log" in text:
        return "log"
    elif "next" in text:
        return "suggest"
    elif "patient" in text:
        return "fetch"
    elif "notify" in text:
        return "notify"
    else:
        return "summarize"


# -------------------------
# BUILD LANGGRAPH
# -------------------------
builder = StateGraph(State)

# Add nodes
builder.add_node("log", log_interaction)
builder.add_node("suggest", suggest_next_step)
builder.add_node("fetch", fetch_patient_info)
builder.add_node("notify", send_notification)
builder.add_node("summarize", summarize)

# Entry point
builder.set_entry_point("log")

# Routing logic
builder.add_conditional_edges(
    "log",
    route_tool,
    {
        "log": "log",
        "suggest": "suggest",
        "fetch": "fetch",
        "notify": "notify",
        "summarize": "summarize",
    }
)

# End node
builder.set_finish_point("summarize")

# Compile graph
graph = builder.compile()
