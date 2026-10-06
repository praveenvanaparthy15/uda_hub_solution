from agentic.state import UDAState


def supervisor_node(state: UDAState) -> UDAState:
    state.setdefault("execution_log", [])
    state.setdefault("messages", [])

    state["execution_log"].append({
        "agent": "supervisor",
        "action": "received_ticket",
        "status": "completed"
    })

    state["messages"].append({
        "role": "supervisor",
        "content": "Ticket received and passed to classifier."
    })

    return state