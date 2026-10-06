# UDA-Hub — Universal Decision Agent

## Overview

UDA-Hub is a multi-agent customer support automation system built using **LangGraph, LangChain, Cohere, RAG, SQLite, and Streamlit**.

The system receives CultPass customer support tickets, understands the issue, routes it to the appropriate specialized agent, retrieves relevant knowledge, uses support tools when required, generates a grounded response, and escalates the ticket when confidence is insufficient.

## Problem Statement

Traditional customer support workflows often require manual ticket classification, knowledge lookup, customer-history checks, and escalation decisions.

UDA-Hub automates this workflow using a multi-agent architecture while maintaining:

* Intelligent ticket classification
* Specialized agent routing
* Retrieval-Augmented Generation (RAG)
* Database-backed support tools
* Short-term session memory
* Long-term customer memory
* Confidence-based escalation
* Structured logging
* Automated tests

## Architecture

The solution follows a **Supervisor + Specialized Agents** architecture.

```text
Customer Support Ticket
        |
        v
   Ticket Data
        |
        v
 Memory Manager
        |
        v
   Supervisor
        |
        v
    Classifier
        |
   +----+----+
   |    |    |
   v    v    v
Billing Technical Account
   |    |    |
   +----+----+
        |
        v
       RAG
        |
        v
 Support Tools
        |
        v
     Resolver
        |
   +----+------+
   |           |
   v           v
Resolved    Escalation
   |           |
   +-----+-----+
         |
         v
   Memory Save
         |
         v
      Logging
```

## Agents

### Supervisor Agent

Coordinates the workflow and passes incoming tickets to the classifier.

### Classifier Agent

Uses Cohere LLM to classify tickets into:

* Billing
* Technical
* Account

It also determines complexity, priority, and classification confidence.

### Billing Agent

Handles billing-related requests using:

* RAG knowledge retrieval
* Refund status tool
* Subscription lookup tool

### Technical Agent

Handles application and technical issues using:

* RAG knowledge retrieval
* Account lookup
* Ticket history

### Account Agent

Handles account-related requests using:

* RAG knowledge retrieval
* Account lookup
* Ticket history

### Resolver Agent

Generates the final customer-facing response using retrieved knowledge and tool results.

The resolver is instructed not to invent policies, refunds, dates, amounts, or account information.

### Escalation Agent

Escalates tickets when:

* Relevant knowledge cannot be found
* Classification confidence is low
* Retrieval confidence is low

## RAG Pipeline

The system contains a CultPass knowledge base with **18 support articles** covering areas such as:

* Account creation
* Password reset
* Login problems
* Subscription plans
* Cancellation
* Renewal
* Refunds
* Payment failures
* Duplicate payments
* Booking problems
* Technical issues
* Profile updates
* Account closure
* Membership pause
* Coupons
* Billing and invoices
* Escalation policy

The RAG pipeline is:

```text
Knowledge Articles
       |
       v
Cohere Embeddings
       |
       v
FAISS Vector Store
       |
       v
Semantic Similarity Search
       |
       v
Relevant Articles
       |
       v
Resolver
```

## Support Tools

The application abstracts database operations through LangChain tools.

### `account_lookup`

Retrieves customer profile and account information.

### `subscription_lookup`

Retrieves customer subscription/account status.

### `refund_status`

Retrieves the current status of a refund-related ticket.

### `ticket_history`

Retrieves previous support tickets for a customer.

These tools access SQLite rather than exposing database operations directly to the agents.

## Memory

UDA-Hub implements two types of memory.

### Short-Term Memory

LangGraph checkpointing with SQLite maintains workflow/session state using `thread_id`.

This allows the same conversation thread to retain state between interactions.

### Long-Term Memory

Customer-specific interaction information is stored in the `CustomerMemory` SQLite table.

This allows future interactions to retrieve previous customer context.

## State Management

The LangGraph state contains information such as:

* Ticket information
* Customer information
* Classification
* Routing
* Retrieved articles
* Tool results
* Short-term memory
* Long-term memory
* Resolution
* Confidence scores
* Escalation information
* Execution logs
* Final response

## Logging

The application produces structured JSON-style logs in:

```text
logs/uda_hub.log
```

The logs capture workflow execution information such as:

* Timestamp
* Agent
* Ticket ID
* Action
* Status
* Tool usage
* Escalation information

## Streamlit Application

A Streamlit UI is provided for submitting customer support tickets.

Run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run 03_agentic_app.py
```

The UI displays:

* Ticket submission
* Category
* Route
* Status
* Customer response
* Escalation status
* Retrieved article count
* Tools used
* Long-term memory count
* Execution details

## Testing

Automated tests are implemented using `pytest`.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

Current test coverage includes:

* Password reset workflow
* Billing workflow
* Technical workflow

All current tests pass successfully.

## Project Structure

```text
uda_hub_solution/
│
├── 03_agentic_app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── agentic/
│   ├── state.py
│   ├── rag.py
│   ├── workflow.py
│   ├── llm.py
│   ├── memory.py
│   ├── ticket_data.py
│   ├── logger.py
│   │
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── classifier.py
│   │   ├── billing.py
│   │   ├── technical.py
│   │   ├── account.py
│   │   ├── resolver.py
│   │   └── escalation.py
│   │
│   ├── tools/
│   │   └── support_tools.py
│   │
│   └── design/
│       ├── architecture.md
│       ├── workflow.md
│       └── rag.md
│
├── data/
│   ├── core/
│   │   ├── database.py
│   │   └── seed_data.py
│   ├── external/
│   └── models/
│
├── tests/
│   └── test_workflow.py
│
└── logs/
```

## Technology Stack

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python     | Application development            |
| LangGraph  | Multi-agent workflow orchestration |
| LangChain  | Agent/tool/RAG framework           |
| Cohere     | LLM and embeddings                 |
| FAISS      | Vector similarity search           |
| SQLite     | Database and persistence           |
| Streamlit  | User interface                     |
| Pytest     | Automated testing                  |
| Pydantic   | Data validation                    |

## Example Workflow

Example input:

```text
Customer: CULT-001
Subject: Password reset
Description: I forgot my password and cannot login.
Channel: chat
Urgency: medium
```

Processing:

```text
Ticket
  ↓
Classifier
  ↓
Account Agent
  ↓
Knowledge Retrieval
  ↓
Resolver
  ↓
Customer Response
```

If the system cannot confidently answer:

```text
Ticket
  ↓
Classifier
  ↓
Specialized Agent
  ↓
RAG
  ↓
Low Confidence
  ↓
Escalation Agent
  ↓
Human Support
```

## Security

Sensitive configuration is stored outside source code using environment variables.

The `.env` file is excluded through `.gitignore`.

Database files, virtual environments, Python cache files, and application logs are also excluded from source control.

## Key Benefits

UDA-Hub demonstrates how agentic AI can combine:

* Multi-agent orchestration
* LLM-based classification
* RAG
* Tool calling
* Database integration
* Memory
* Confidence-based decision making
* Human escalation
* Observability
* Automated testing

This provides an end-to-end example of an enterprise-style AI customer support decision system.
