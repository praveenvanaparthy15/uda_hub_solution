import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from langgraph.graph import StateGraph, START, END

from agentic.state import UDAState
from agentic.agents.supervisor import supervisor_node
from agentic.agents.classifier import classifier_node
from agentic.agents.billing import billing_node
from agentic.agents.technical import technical_node
from agentic.agents.account import account_node
from agentic.agents.resolver import resolver_node
from agentic.agents.escalation import escalation_node
from agentic.memory import load_memory_into_state, save_state_memory
from agentic.ticket_data import load_ticket_data
from agentic.logger import log_event

def route_ticket(state: UDAState) -> str:
    category = state.get("category", "account")

    if category == "billing":
        return "billing"

    if category == "technical":
        return "technical"

    return "account"


def route_after_resolver(state: UDAState) -> str:
    if state.get("status") == "needs_escalation":
        return "escalation"

    return "end"

CHECKPOINT_DB = "data/core/checkpoints.db"

conn = sqlite3.connect(
    CHECKPOINT_DB,
    check_same_thread=False
)

checkpointer = SqliteSaver(conn)

def logging_node(state: UDAState) -> UDAState:
    """Record the current workflow execution."""

    log_event(
        message=f"Workflow processed ticket with status: {state.get('status')}",
        agent="workflow",
        ticket_id=state.get("ticket_id"),
    )

    return state


builder = StateGraph(UDAState)

# Agents
builder.add_node("supervisor", supervisor_node)
builder.add_node("classifier", classifier_node)
builder.add_node("billing", billing_node)
builder.add_node("technical", technical_node)
builder.add_node("account", account_node)
builder.add_node("resolver", resolver_node)
builder.add_node("escalation", escalation_node)

builder.add_node("memory_load", load_memory_into_state)
builder.add_node("memory_save", save_state_memory)
builder.add_node("ticket_data", load_ticket_data)

# Entry
builder.add_edge(START, "ticket_data")
builder.add_edge("ticket_data", "memory_load")
builder.add_edge("memory_load", "supervisor")
builder.add_node("logging", logging_node)


# Classification
builder.add_edge("supervisor", "classifier")

# Routing
builder.add_conditional_edges(
    "classifier",
    route_ticket,
    {
        "billing": "billing",
        "technical": "technical",
        "account": "account",
    },
)

# Specialized agents → Resolver
builder.add_edge("billing", "resolver")
builder.add_edge("technical", "resolver")
builder.add_edge("account", "resolver")

# Resolver → Resolve OR Escalate
builder.add_conditional_edges(
    "resolver",
    route_after_resolver,
    {
        "end": "memory_save",
        "escalation": "escalation",
    },
)

builder.add_edge("escalation", "memory_save")
builder.add_edge("memory_save", "logging")
builder.add_edge("logging", END)

# Escalation → End
builder.add_edge("escalation", END)

#workflow = builder.compile()
workflow = builder.compile(checkpointer=checkpointer)