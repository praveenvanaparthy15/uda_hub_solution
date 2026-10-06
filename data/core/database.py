import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "uda_hub.db"


def get_connection():
    """Create a connection to the UDA-Hub SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all required UDA-Hub database tables."""

    connection = get_connection()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS Account (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            platform TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            external_user_id TEXT UNIQUE,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id)
                REFERENCES Account(account_id)
        );

        CREATE TABLE IF NOT EXISTS Ticket (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT,
            description TEXT NOT NULL,
            channel TEXT,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES User(user_id)
        );

        CREATE TABLE IF NOT EXISTS TicketMetadata (
            metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            urgency TEXT,
            category TEXT,
            priority TEXT,
            source_platform TEXT,
            FOREIGN KEY (ticket_id)
                REFERENCES Ticket(ticket_id)
        );

        CREATE TABLE IF NOT EXISTS TicketMessage (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            sender_type TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id)
                REFERENCES Ticket(ticket_id)
        );

        CREATE TABLE IF NOT EXISTS Knowledge (
            knowledge_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS CustomerMemory (
            memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            memory TEXT NOT NULL,
            source_ticket_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_ticket_id)
                REFERENCES Ticket(ticket_id)
        );

        """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized successfully: {DB_PATH}")