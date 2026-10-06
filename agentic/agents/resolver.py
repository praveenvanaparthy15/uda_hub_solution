from agentic.state import UDAState
from agentic.llm import llm


RAG_CONFIDENCE_THRESHOLD = 0.45
CLASSIFICATION_CONFIDENCE_THRESHOLD = 0.60


def resolver_node(state: UDAState) -> UDAState:
    """Create a grounded customer-facing resolution."""

    articles = state.get("retrieved_articles", [])
    classification_confidence = state.get(
        "classification_confidence", 0.0
    )

    if not articles:
        state["resolution"] = None
        state["resolution_confidence"] = 0.0
        state["status"] = "needs_escalation"
        state["escalation_reason"] = (
            "No relevant knowledge article was found."
        )

        state.setdefault("execution_log", []).append(
            {
                "agent": "resolver",
                "action": "no_knowledge_found",
                "status": "escalation_required",
            }
        )

        return state

    # FAISS returns distance scores.
    # Lower distance means better similarity.
    best_score = articles[0].get("score", 999.0)

    rag_confidence = 1.0 / (1.0 + best_score)

    state["retrieval_confidence"] = rag_confidence

    if (
        rag_confidence < RAG_CONFIDENCE_THRESHOLD
        or classification_confidence < CLASSIFICATION_CONFIDENCE_THRESHOLD
    ):
        state["resolution"] = None
        state["resolution_confidence"] = min(
            rag_confidence,
            classification_confidence,
        )
        state["status"] = "needs_escalation"
        state["escalation_reason"] = (
            "Low confidence in ticket classification or "
            "knowledge retrieval."
        )

        state.setdefault("execution_log", []).append(
            {
                "agent": "resolver",
                "action": "low_confidence",
                "rag_confidence": rag_confidence,
                "classification_confidence": classification_confidence,
                "status": "escalation_required",
            }
        )

        return state

    top_articles = "\n\n".join(
        [
            f"Article: {article['title']}\n"
            f"Category: {article['category']}\n"
            f"Content: {article['content']}"
            for article in articles
        ]
    )

    tool_results = state.get("tool_results", [])

    prompt = f"""
You are the Resolver Agent for CultPass customer support.

Create a concise, professional customer-facing response.

Customer:
{state.get('customer', {})}

Customer ID:
{state.get('customer_id', '')}

Ticket subject:
{state.get('subject', '')}

Ticket description:
{state.get('description', '')}

Relevant CultPass knowledge:
{top_articles}

Previous customer interactions:
{state.get('long_term_memory', [])}

Support tool results:
{tool_results}

Instructions:
1. Answer only using the supplied knowledge and tool results.
2. Do not invent policies, refunds, dates, amounts, or account details.
3. Give clear practical next steps when available.
4. Keep the response concise.
5. If the available information does not support a definitive answer,
   say that human support may need to review it.
"""

    response = llm.invoke(prompt)

    state["resolution"] = response.content
    state["final_response"] = response.content
    state["resolution_confidence"] = min(
        rag_confidence,
        classification_confidence,
    )
    state["status"] = "resolved"

    state.setdefault("execution_log", []).append(
        {
            "agent": "resolver",
            "action": "llm_grounded_resolution_created",
            "article": articles[0]["title"],
            "rag_confidence": rag_confidence,
            "classification_confidence": classification_confidence,
            "status": "completed",
        }
    )

    state.setdefault("messages", []).append(
        {
            "role": "resolver",
            "content": "LLM-generated grounded customer response created.",
        }
    )

    return state