from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class UDAState(TypedDict, total=False):
    # ---------------------------------------------------------
    # Incoming ticket
    # ---------------------------------------------------------
    thread_id: Optional[str]
    ticket_id: Optional[int]
    customer_id: Optional[str]
    channel: Optional[str]
    subject: Optional[str]
    description: Optional[str]
    urgency: Optional[str]
    priority: Optional[str]
    

    # ---------------------------------------------------------
    # Customer information
    # ---------------------------------------------------------
    customer: Dict[str, Any]

    # ---------------------------------------------------------
    # Classification and routing
    # ---------------------------------------------------------
    category: Optional[str]
    complexity: Optional[str]
    classification_confidence: float
    route: Optional[str]

    # ---------------------------------------------------------
    # Memory
    # ---------------------------------------------------------
    short_term_memory: List[Dict[str, Any]]
    long_term_memory: List[Dict[str, Any]]

    # ---------------------------------------------------------
    # Knowledge retrieval
    # ---------------------------------------------------------
    retrieved_articles: List[Dict[str, Any]]
    retrieval_confidence: float

    # ---------------------------------------------------------
    # Tool execution
    # ---------------------------------------------------------
    tool_results: List[Dict[str, Any]]

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------
    resolution: Optional[str]
    resolution_confidence: float

    # ---------------------------------------------------------
    # Escalation
    # ---------------------------------------------------------
    escalated: bool
    escalation_reason: Optional[str]
    escalation_summary: Optional[str]

    # ---------------------------------------------------------
    # Final response
    # ---------------------------------------------------------
    final_response: Optional[str]
    status: Optional[str]

    # ---------------------------------------------------------
    # Agent messages / execution trace
    # ---------------------------------------------------------
    messages: List[Dict[str, Any]]
    execution_log: List[Dict[str, Any]]