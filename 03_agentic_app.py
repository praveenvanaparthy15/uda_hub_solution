import streamlit as st

from agentic.workflow import workflow


st.set_page_config(
    page_title="UDA-Hub",
    page_icon="🎫",
    layout="wide",
)


st.title("UDA-Hub — Universal Decision Agent")
st.caption("Multi-agent CultPass Customer Support Automation")


if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit-session-001"


st.subheader("Create Support Ticket")

customer_id = st.text_input(
    "Customer ID",
    value="CULT-001",
)

subject = st.text_input(
    "Subject",
    value="Password reset",
)

description = st.text_area(
    "Describe your issue",
    value="I forgot my CultPass password and cannot login.",
)

channel = st.selectbox(
    "Channel",
    ["chat", "email", "phone", "web"],
)

urgency = st.selectbox(
    "Urgency",
    ["low", "medium", "high", "critical"],
)

if st.button("Submit Ticket", type="primary"):

    input_state = {
        "thread_id": st.session_state.thread_id,
        "customer_id": customer_id,
        "subject": subject,
        "description": description,
        "channel": channel,
        "urgency": urgency,
        "messages": [],
        "execution_log": [],
    }

    with st.spinner("UDA-Hub agents are processing your ticket..."):

        config = {
            "configurable": {
                "thread_id": st.session_state.thread_id
            }
        }

        result = workflow.invoke(
            input_state,
            config
        )

    st.success("Ticket processed")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Category",
            result.get("category", "N/A")
        )

    with col2:
        st.metric(
            "Route",
            result.get("route", "N/A")
        )

    with col3:
        st.metric(
            "Status",
            result.get("status", "N/A")
        )

    st.subheader("Customer Response")

    st.write(
        result.get(
            "final_response",
            result.get(
                "resolution",
                "No response generated."
            ),
        )
    )

    if result.get("escalated"):
        st.warning(
            "This ticket has been escalated to human support."
        )

    with st.expander("Execution Details"):

        st.write(
            "Thread ID:",
            st.session_state.thread_id
        )

        st.write(
            "Retrieved Articles:",
            len(result.get("retrieved_articles", []))
        )

        st.write(
            "Tools Used:",
            [
                item.get("tool")
                for item in result.get("tool_results", [])
            ]
        )

        st.write(
            "Long-term Memories:",
            len(result.get("long_term_memory", []))
        )

        st.json(
            result.get("execution_log", [])
        )