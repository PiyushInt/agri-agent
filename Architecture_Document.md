# 🏗️ Architecture Document: Agricultural Advisory Agent

## System Overview Overview
The Agricultural Advisory Agent is designed with a strict emphasis on compliance, guardrail enforcement, and auditability. It operates on a ReAct (Reasoning and Acting) framework, intercepted by dedicated policy guards.

## Architecture Diagram

```mermaid
graph TD
    User([Farmer / User]) -->|1. Prompts| UI[Streamlit UI]
    
    subgraph "Compliance Layer"
        UI -->|2. Check Input| InputGuard[Input Guardrail]
        OutputGuard[Output Guardrail] -->|8. Clean Response| UI
    end
    
    subgraph "Core Agent Logic"
        InputGuard -->|3. Safe Prompt| Agent[ReAct Agent]
        Agent -->|6. Draft Response| OutputGuard
    end
    
    subgraph "Tool Integration Ecosystem"
        Agent <-->|4. Fetch Data| Tools[Mock Environment Tools]
        Tools --> Weather[Weather API]
        Tools --> Soil[Soil API]
        Tools --> Market[Market Price API]
        Tools --> Chem[Approved Chemicals API]
    end
    
    subgraph "Auditability"
        UI -.->|Logs Prompt| Audit[(Audit Logger SQLite)]
        InputGuard -.->|Logs Safety Check| Audit
        Agent -.->|Logs Thoughts| Audit
        Tools -.->|Logs Execution| Audit
        OutputGuard -.->|Logs Modifications| Audit
    end

    classDef guard fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef agent fill:#ccddff,stroke:#0055ff,stroke-width:2px;
    classDef database fill:#e6ffe6,stroke:#00ff00,stroke-width:2px;
    
    class InputGuard,OutputGuard guard;
    class Agent agent;
    class Audit database;
```

## Component Roles & Communication

### 1. The Compliance Guardrails (Input/Output Interceptors)
- **Role:** Enforces regulatory and domain policies before the LLM processes data or the user sees the output.
- **Communication:** Synchronous interception. If the user asks for restricted chemicals or non-agricultural topics, the `Input Guardrail` blocks the request entirely. If the LLM generates a response containing a locally banned chemical (e.g., DDT), the `Output Guardrail` catches it, modifies the text, appends a legal disclaimer, and passes it to the UI.

### 2. Core ReAct Agent (LangChain)
- **Role:** The reasoning engine. It breaks down complex queries (e.g., "What to plant in region_1 tomorrow?") and decides which tools to invoke.
- **Error Handling logic:** If a tool fails or returns empty data, the ReAct loop catches the parsing error and asks the LLM to rethink or ask the user for clarification.

### 3. Tool Integrations
- **Role:** Simulate external data retrieval (Sensors, Weather Stations, Government Databases).
- **Integration:** The tools are bound as LangChain tools. They are invoked by the Agent dynamically based on the Thought/Action cycle.

### 4. Immutable Audit Logger
- **Role:** Ensures 100% accountability. 
- **Communication:** Receives asynchronous push-events from the UI, Guardrails, Tools, and Agent. It stores JSON payloads of every action to `audit_log.db` to prove compliance to auditors.
