from agentic.state import UDAState
from agentic.rag import search_knowledge
from agentic.tools.support_tools import refund_status, subscription_lookup


def billing_node(state: UDAState) -> UDAState:
    query = f"""
    Customer billing issue:
    Subject: {state.get('subject', '')}
    Description: {state.get('description', '')}
    """

    articles = search_knowledge(query)

    tool_results = []

    ticket_id = state.get("ticket_id")
    customer_id = state.get("customer_id")

    if ticket_id is not None:
        tool_results.append(
            {
                "tool": "refund_status",
                "result": refund_status.invoke({"ticket_id": ticket_id}),
            }
        )

    if customer_id:
        tool_results.append(
            {
                "tool": "subscription_lookup",
                "result": subscription_lookup.invoke(
                    {"customer_id": customer_id}
                ),
            }
        )

    state["route"] = "billing"
    state["retrieved_articles"] = articles
    state["tool_results"] = tool_results

    state.setdefault("execution_log", []).append(
        {
            "agent": "billing",
            "action": "billing_rag_and_tools",
            "articles_found": len(articles),
            "tools_used": [item["tool"] for item in tool_results],
            "status": "completed",
        }
    )

    state.setdefault("messages", []).append(
        {
            "role": "billing",
            "content": (
                f"Billing agent searched {len(articles)} knowledge articles "
                f"and invoked {len(tool_results)} support tools."
            ),
        }
    )

    return state