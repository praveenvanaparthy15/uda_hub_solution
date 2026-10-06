from agentic.state import UDAState
from agentic.rag import search_knowledge
from agentic.tools.support_tools import account_lookup, ticket_history


def account_node(state: UDAState) -> UDAState:
    query = f"""
    Customer account issue:
    Subject: {state.get('subject', '')}
    Description: {state.get('description', '')}
    """

    articles = search_knowledge(query)

    tool_results = []
    customer_id = state.get("customer_id")

    if customer_id:
        tool_results.append(
            {
                "tool": "account_lookup",
                "result": account_lookup.invoke(
                    {"customer_id": customer_id}
                ),
            }
        )

        tool_results.append(
            {
                "tool": "ticket_history",
                "result": ticket_history.invoke(
                    {"customer_id": customer_id}
                ),
            }
        )

    state["route"] = "account"
    state["retrieved_articles"] = articles
    state["tool_results"] = tool_results

    state.setdefault("execution_log", []).append(
        {
            "agent": "account",
            "action": "account_rag_and_tools",
            "articles_found": len(articles),
            "tools_used": [item["tool"] for item in tool_results],
            "status": "completed",
        }
    )

    state.setdefault("messages", []).append(
        {
            "role": "account",
            "content": (
                f"Account agent searched {len(articles)} knowledge articles "
                f"and invoked {len(tool_results)} support tools."
            ),
        }
    )

    return state