from pathlib import Path
import sqlite3

from agentic.state import UDAState


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "core"
    / "uda_hub.db"
)


def load_ticket_data(state: UDAState) -> UDAState:
    """Load ticket and metadata information from SQLite."""

    ticket_id = state.get("ticket_id")

    if ticket_id is None:
        return state

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    ticket = connection.execute(
        """
        SELECT
            t.ticket_id,
            t.user_id,
            t.subject,
            t.description,
            t.channel,
            t.status,
            u.external_user_id
        FROM Ticket t
        JOIN User u
            ON t.user_id = u.user_id
        WHERE t.ticket_id = ?
        """,
        (ticket_id,),
    ).fetchone()

    metadata = connection.execute(
        """
        SELECT
            urgency,
            category,
            priority,
            source_platform
        FROM TicketMetadata
        WHERE ticket_id = ?
        ORDER BY metadata_id DESC
        LIMIT 1
        """,
        (ticket_id,),
    ).fetchone()

    connection.close()

    if ticket:
        state["ticket_id"] = ticket["ticket_id"]
        state["customer_id"] = ticket["external_user_id"]
        state["subject"] = ticket["subject"]
        state["description"] = ticket["description"]
        state["channel"] = ticket["channel"]

    if metadata:
        state["urgency"] = metadata["urgency"]
        state["priority"] = metadata["priority"]

        if metadata["category"]:
            state["category"] = metadata["category"]

        state["source_platform"] = metadata["source_platform"]

    state.setdefault("execution_log", []).append(
        {
            "agent": "ticket_data",
            "action": "ticket_and_metadata_loaded",
            "ticket_id": ticket_id,
            "metadata_found": metadata is not None,
            "status": "completed",
        }
    )

    return state