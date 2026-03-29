import streamlit as st
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from src.audit_logger import AuditLogger
from src.guardrails import AgriculturalGuardrails
from src.agent import AgriculturalAgent
import os
from dotenv import load_dotenv

# Load secret API keys from the local .env file
load_dotenv() 

st.set_page_config(page_title="AgriAdviser AI", layout="centered")

st.title("🌾 Agricultural Advisory AI Agent")

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

session_id = st.session_state["session_id"]
logger = AuditLogger()
guardrails = AgriculturalGuardrails(logger)

# UI layout
st.subheader("Chat Interface")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome! I am your Agricultural AI Advisor. How can I help you today?"}]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("E.g., What fertilizer should I use for cotton in region_1?"):
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    logger.log_user_prompt(session_id, prompt)
    
    # 1. Input Guardrail
    if not guardrails.check_input(session_id, prompt):
        block_msg = "Your input triggered a security guardrail. Request blocked."
        st.chat_message("assistant").error(block_msg)
        st.session_state["messages"].append({"role": "assistant", "content": block_msg})
    else:
        # Check environment variables for API keys
        google_key = os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if not google_key and not openai_key:
            st.error("Missing API Key! Please add GOOGLE_API_KEY or OPENAI_API_KEY to your local `.env` file.")
        else:
            with st.spinner("Analyzing soil, weather, & market data..."):
                try:
                    if google_key:
                        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)
                    else:
                        llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

                    agent = AgriculturalAgent(llm, logger, session_id)
                    raw_output = agent.run(prompt)
                    
                    # 2. Output Guardrail Check
                    final_response = guardrails.check_output(session_id, raw_output)
                    
                    logger.log_final_response(session_id, final_response)
                    
                    st.chat_message("assistant").write(final_response)
                    st.session_state["messages"].append({"role": "assistant", "content": final_response})
                except Exception as e:
                    st.error(f"Error communicating with AI: {e}")
