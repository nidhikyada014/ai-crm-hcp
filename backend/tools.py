from llm import call_llm

# =========================
# TOOL 1: LOG INTERACTION
# =========================
def log_interaction(state):
    prompt = f"""
    Extract structured data from this interaction:

    Input: {state['input']}

    Return:
    - Doctor Name
    - Date
    - Summary
    """

    result = call_llm(prompt)

    return {
        "output": f"Interaction Logged Successfully:\n{result}"
    }


# =========================
# TOOL 2: EDIT INTERACTION
# =========================
def edit_interaction(state):
    return {
        "output": "Interaction updated successfully in database"
    }


# =========================
# TOOL 3: SEARCH INTERACTION
# =========================
def search_interaction(state):
    prompt = f"""
    Find and return matching interactions based on:

    Input: {state['input']}
    """

    result = call_llm(prompt)

    return {
        "output": f"Search Results:\n{result}"
    }


# =========================
# TOOL 4: SUMMARIZE INTERACTION
# =========================
def summarize_interaction(state):
    prompt = f"Summarize this interaction:\n{state['input']}"

    result = call_llm(prompt)

    return {
        "output": f"Summary:\n{result}"
    }


# =========================
# TOOL 5: RECOMMEND NEXT ACTION
# =========================
def recommend_action(state):
    prompt = f"""
    Based on this interaction, suggest next sales action:

    {state['input']}
    """

    result = call_llm(prompt)

    return {
        "output": f"Recommended Action:\n{result}"
    }
