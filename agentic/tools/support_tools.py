from pathlib import Path
import sqlite3

from langchain_core.tools import tool


DB_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "core"
    / "uda_hub.db"
)


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@tool
def account_lookup(customer_id: str) -> dict:
    """Retrieve customer account and profile information."""

    conn = _get_connection()

    row = conn.execute(
        """
        SELECT
            u.user_id,
            u.external_user_id,
            u.name,
            u.email,
            a.account_id,
            a.account_name,
            a.platform,
            a.status AS account_status
        FROM User u
        JOIN Account a
            ON u.account_id = a.account_id
        WHERE u.external_user_id = ?
        """,
        (customer_id,)
    ).fetchone()

    conn.close()

    if not row:
        return {
            "found": False,
            "message": "Customer not found."
        }

    return {
        "found": True,
        "user_id": row["user_id"],
        "customer_id": row["external_user_id"],
        "name": row["name"],
        "email": row["email"],
        "account_id": row["account_id"],
        "account_name": row["account_name"],
        "platform": row["platform"],
        "account_status": row["account_status"]
    }


@tool
def subscription_lookup(customer_id: str) -> dict:
    """Retrieve subscription/account status for a customer."""

    conn = _get_connection()

    row = conn.execute(
        """
        SELECT
            u.external_user_id,
            a.account_name,
            a.platform,
            a.status
        FROM User u
        JOIN Account a
            ON u.account_id = a.account_id
        WHERE u.external_user_id = ?
        """,
        (customer_id,)
    ).fetchone()

    conn.close()

    if not row:
        return {
            "found": False,
            "message": "Subscription information not found."
        }

    return {
        "found": True,
        "customer_id": row["external_user_id"],
        "account_name": row["account_name"],
        "platform": row["platform"],
        "subscription_status": row["status"],
        "note": "Detailed plan and renewal information is not stored in the current database schema."
    }


@tool
def refund_status(ticket_id: int) -> dict:
    """Retrieve the current status of a refund-related support ticket."""

    conn = _get_connection()

    row = conn.execute(
        """
        SELECT
            ticket_id,
            subject,
            description,
            status,
            channel,
            created_at
        FROM Ticket
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    ).fetchone()

    conn.close()

    if not row:
        return {
            "found": False,
            "message": "Ticket not found."
        }

    return {
        "found": True,
        "ticket_id": row["ticket_id"],
        "subject": row["subject"],
        "description": row["description"],
        "ticket_status": row["status"],
        "channel": row["channel"],
        "created_at": row["created_at"]
    }


@tool
def ticket_history(customer_id: str) -> list:
    """Retrieve previous support tickets for a customer."""

    conn = _get_connection()

    rows = conn.execute(
        """
        SELECT
            t.ticket_id,
            t.subject,
            t.description,
            t.channel,
            t.status,
            t.created_at
        FROM Ticket t
        JOIN User u
            ON t.user_id = u.user_id
        WHERE u.external_user_id = ?
        ORDER BY t.created_at DESC, t.ticket_id DESC
        """,
        (customer_id,)
    ).fetchall()

    conn.close()

    return [
        {
            "ticket_id": row["ticket_id"],
            "subject": row["subject"],
            "description": row["description"],
            "channel": row["channel"],
            "status": row["status"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]