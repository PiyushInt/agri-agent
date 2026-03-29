from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from src.audit_logger import AuditLogger
from src import tools as domain_tools

class AgriculturalAgent:
    def __init__(self, llm, logger: AuditLogger, session_id: str):
        self.llm = llm
        self.logger = logger
        self.session_id = session_id
        
        # Define Tools
        @tool
        def get_weather(location_id: str) -> str:
            """Fetch the weather forecast for a given location_id. e.g., 'region_1'"""
            res = domain_tools.get_weather_forecast(location_id)
            self.logger.log_tool_execution(self.session_id, "get_weather", {"location_id": location_id}, res)
            return res

        @tool
        def get_soil(location_id: str) -> str:
            """Fetch local soil condition such as pH, nitrogen missing, moisture for 'region_1' or 'region_2'."""
            res = domain_tools.get_soil_data(location_id)
            self.logger.log_tool_execution(self.session_id, "get_soil", {"location_id": location_id}, res)
            return res
            
        @tool
        def get_market_price(crop: str) -> str:
            """Fetch current market price for a given crop like 'wheat', 'rice', or 'cotton'."""
            res = domain_tools.get_market_prices(crop)
            self.logger.log_tool_execution(self.session_id, "get_market_price", {"crop": crop}, res)
            return res

        @tool
        def list_approved_chemicals(crop: str) -> str:
            """Fetch locally approved agricultural chemicals/fertilizers for a given crop. MUST BE USED BEFORE PRESCRIBING ANY CHEMICAL."""
            res = domain_tools.list_approved_chemicals(crop)
            self.logger.log_tool_execution(self.session_id, "list_approved_chemicals", {"crop": crop}, res)
            return res

        self.tools = [get_weather, get_soil, get_market_price, list_approved_chemicals]
        
        system_message = '''Answer the following questions as best you can. You are an Agricultural Advisory AI expert serving rural farmers. 
Your goal is to provide actionable guidance balancing local weather, soil, and market prices constraints. 
Always recommend *only* approved chemicals.

You MUST use tools when possible to look up approved chemicals before recommending them.
'''
        
        self.agent_executor = create_react_agent(self.llm, self.tools, prompt=system_message)

    def run(self, query: str) -> str:
        self.logger.log_agent_thought(self.session_id, f"Initiating ReAct Loop for query: '{query}'")
        try:
            result = self.agent_executor.invoke({"messages": [("user", query)]})
            final_answer = result["messages"][-1].content
            return final_answer
        except Exception as e:
            self.logger.log_agent_thought(self.session_id, f"Error encountering processing: {str(e)}")
            return "Apologies, I encountered an internal error processing the agricultural rules."
