from pathlib import Path
import sqlite3

from agentic.state import UDAState


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "core"
    / "uda_hub.db"
)


def save_memory(
    customer_id: str,
    memory: str,
    source_ticket_id: int | None = None,
) -> None:
    """Persist a customer memory in SQLite."""

    if not customer_id or not memory:
        return

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        """
        INSERT INTO CustomerMemory (
            customer_id,
            memory,
            source_ticket_id
        )
        VALUES (?, ?, ?)
        """,
        (
            customer_id,
            memory,
            source_ticket_id,
        ),
    )

    connection.commit()
    connection.close()


def load_memories(
    customer_id: str,
    limit: int = 10,
) -> list[dict]:
    """Load recent long-term memories for a customer."""

    if not customer_id:
        return []

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT
            memory_id,
            customer_id,
            memory,
            source_ticket_id,
            created_at
        FROM CustomerMemory
        WHERE customer_id = ?
        ORDER BY created_at DESC, memory_id DESC
        LIMIT ?
        """,
        (
            customer_id,
            limit,
        ),
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def load_memory_into_state(state: UDAState) -> UDAState:
    """Load persistent customer memories into the LangGraph state."""

    customer_id = state.get("customer_id")

    memories = load_memories(customer_id)

    state["long_term_memory"] = memories

    state.setdefault("execution_log", []).append(
        {
            "agent": "memory_manager",
            "action": "long_term_memory_loaded",
            "customer_id": customer_id,
            "memories_found": len(memories),
            "status": "completed",
        }
    )

    return state


def save_state_memory(state: UDAState) -> UDAState:
    """Save the current interaction as long-term customer memory."""

    customer_id = state.get("customer_id")

    if not customer_id:
        return state

    ticket_id = state.get("ticket_id")

    memory_text = (
        f"Ticket subject: {state.get('subject', '')}. "
        f"Category: {state.get('category', '')}. "
        f"Resolution status: {state.get('status', '')}."
    )

    save_memory(
        customer_id=customer_id,
        memory=memory_text,
        source_ticket_id=ticket_id,
    )

    state.setdefault("execution_log", []).append(
        {
            "agent": "memory_manager",
            "action": "long_term_memory_saved",
            "customer_id": customer_id,
            "status": "completed",
        }
    )

    return state