# 🌾 Agricultural Advisory Agent

**A Domain-Specialized AI Agent with Strict Compliance Guardrails and 100% Auditability.**

This prototype was built specifically to address the hackathon challenge for creating domain-specific AI agents that execute workflows, handle edge cases, and stay within regulatory and policy guardrails at all times.

## 🎯 Evaluation Focus Addressed
- **Domain Expertise Depth:** The agent specializes purely in agricultural advisory, using localized tools to synthesize weather, soil data, and market prices to provide tailored farming advice.
- **Compliance & Guardrail Enforcement:** A standalone Guardrails layer explicitly checks user inputs for malicious requests and prevents the agent from recommending banned chemical fertilizers (e.g., DDT). It seamlessly appends necessary legal/safety disclaimers to every response.
- **Auditability of Every Agent Decision:** Driven by an immutable `AuditLogger`, 100% of session requests, tool executions, guardrail interceptions, and thought processes are written into a backend SQLite database and visualized live in the UI.

---

## 🏗 Architecture Components

1. **ReAct Logic Engine (`agent.py`)**: Built with LangChain, this connects the underlying LLM to custom IoT/environmental tools. E.g., determining whether to fetch weather forecasts before giving fertilization advice.
2. **Mock Tools Ecosystem (`tools.py`)**: Designed to simulate connected agricultural sensors and databases, featuring:
   - `get_soil_data(location_id)`
   - `get_weather_forecast(location_id)`
   - `get_market_prices(crop)`
   - `list_approved_chemicals(crop)`
3. **Immutable Auditing System (`audit_logger.py`)**: Creates and persists an SQLite `audit_log.db` recording timestamps, event types, and exact payload JSONs.
4. **Policy Guardrails (`guardrails.py`)**: An interception engine strictly enforcing domain rules over LLM inputs and outputs.
5. **Interactive UI (`app.py`)**: A Streamlit interface demonstrating the agent chat alongside a scrolling real-time view of the Immutable Audit Trail.

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- A Google GenAI or OpenAI API Key (configured securely through the App UI)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/PiyushInt/agri-agent.git
   cd agri-agent
   ```
   
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit Application:
   ```bash
   streamlit run app.py
   ```

### Live Demonstration Ideas
- **Test Contextual Thinking**: Ask what fertilizer to use for "cotton" in "region_1". Watch the Audit Log as the agent consults both weather tools and approved chemicals before answering.
- **Test Input Filtering**: Try asking the agent to help build a bomb or something explicitly out-of-domain.
- **Test Output Re-formatting**: Any advice automatically gets an explicit warning disclaimer appended by the independent Guardrails engine.

> **Note:** The `audit_log.db` database is dynamically generated during the session internally.
