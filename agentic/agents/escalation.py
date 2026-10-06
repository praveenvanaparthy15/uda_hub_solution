from agentic.state import UDAState


def escalation_node(state: UDAState) -> UDAState:
    """Escalate tickets that cannot be safely resolved."""

    reason = state.get(
        "escalation_reason",
        "Insufficient confidence or knowledge."
    )

    state["escalated"] = True
    state["status"] = "escalated"

    state["escalation_reason"] = reason

    state["escalation_summary"] = (
        f"Ticket {state.get('ticket_id', 'N/A')} "
        f"requires human support. Reason: {reason}"
    )

    state["final_response"] = (
        "I’m unable to confidently resolve this request from "
        "the available CultPass support information. "
        "Your ticket has been escalated to a human support specialist."
    )

    state.setdefault("execution_log", []).append({
        "agent": "escalation",
        "action": "ticket_escalated",
        "reason": reason,
        "status": "completed"
    })

    state.setdefault("messages", []).append({
        "role": "escalation",
        "content": "Ticket escalated to human support."
    })

    return state