from agentic.workflow import workflow


def test_password_reset_workflow():
    state = {
        "thread_id": "test-password-001",
        "customer_id": "CULT-001",
        "subject": "Password reset",
        "description": "I forgot my password and cannot login.",
        "channel": "chat",
        "urgency": "medium",
        "messages": [],
        "execution_log": [],
    }

    result = workflow.invoke(
        state,
        {"configurable": {"thread_id": "test-password-001"}}
    )

    assert result.get("status") in ["resolved", "escalated"]
    assert result.get("final_response")


def test_billing_workflow():
    state = {
        "thread_id": "test-billing-001",
        "customer_id": "CULT-002",
        "subject": "Payment failed",
        "description": "My payment failed while purchasing CultPass.",
        "channel": "chat",
        "urgency": "high",
        "messages": [],
        "execution_log": [],
    }

    result = workflow.invoke(
        state,
        {"configurable": {"thread_id": "test-billing-001"}}
    )

    assert result.get("status") in ["resolved", "escalated"]
    assert result.get("final_response")


def test_technical_workflow():
    state = {
        "thread_id": "test-technical-001",
        "customer_id": "CULT-003",
        "subject": "Application not working",
        "description": "The CultPass application is not opening.",
        "channel": "mobile",
        "urgency": "high",
        "messages": [],
        "execution_log": [],
    }

    result = workflow.invoke(
        state,
        {"configurable": {"thread_id": "test-technical-001"}}
    )

    assert result.get("status") in ["resolved", "escalated"]
    assert result.get("final_response")