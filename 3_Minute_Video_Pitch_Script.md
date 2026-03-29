# 🎥 3-Minute Pitch Video Script

**Title:** Agri-Agent: Auditable Farming Intelligence

---

### [0:00 - 0:30] The Problem
**Visual:** Show the Streamlit UI loading screen, or a slide of farmers struggling with crop data.
**Voiceover:** "Hello! Imagine you are a farmer in a rural area. Getting advice on which fertilizer to apply based on your local soil takes days of waiting for an expert. Worse, if you apply the wrong chemical—like a locally banned pesticide—your entire crop could be rejected by buyers. Agricultural AI has huge potential here, but LLMs alone are prone to hallucination, breaking compliance, and offering dangerous chemicals. We need something safer."

### [0:30 - 1:15] The Solution & Architecture
**Visual:** Show the Architecture Diagram (`Architecture_Document.md`) highlighting the Guardrails and Audit Logger.
**Voiceover:** "Enter the Agri-Agent. We built a domain-specialized AI agent focused entirely on compliance and edge-case handling. What makes us different? We wrapped our ReAct-based Agent inside a strict **Guardrails Engine**. Before an LLM processes a prompt, or outputs an answer, it is intercepted and scrubbed. Furthermore, every single decision our agent makes is recorded immutably via our SQLite Audit Logger. Let’s see it live."

### [1:15 - 2:00] Demo Highlight 1: The Workflow & Auditability
**Visual:** Start recording the Streamlit App (`app.py`). Type: "What fertilizer should I use for cotton in region_1?"
**Voiceover:** "Here, I ask for cotton fertilizer. You'll see the agent dynamically triggers our simulated tools: checking regional weather, pulling local soil data, and querying the approved chemicals list. On the right, our live Immutable Audit Trail proves exactly why it made its final choice, ensuring 100% accountability for the judges."

### [2:00 - 2:30] Demo Highlight 2: Guardrails & Edge Cases
**Visual:** Type an edge-case prompt: "How do I make a bomb?" (Shows input block). Then highlight the disclaimer at the bottom of the previous answer.
**Voiceover:** "Look what happens if an out-of-domain edge case is hit: The Input Guardrail immediately blocks it. You’ll also notice every legitimate answer automatically gets a safety disclaimer appended by the Output Guardrail. If the LLM ever tried to recommend a banned substance like DDT, our engine intercepts it and rewrites the advice to keep the farmer compliant."

### [2:30 - 3:00] The Business Impact
**Visual:** Show the Impact Model document highlighting the $1M in savings.
**Voiceover:** "The impact is massive. As detailed in our Impact Model, for just 10,000 farmers, decreasing consultation time from 3 days to 10 seconds saves $500,000 in logistical costs, and our guardrails protect an estimated $500,000 in lost crop yields from unapproved fertilizers. We've built an AI that doesn’t just answer questions—it protects the farmer, auditably and compliantly. Thank you!"
