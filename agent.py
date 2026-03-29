from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from audit_logger import AuditLogger
import tools as domain_tools

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
        
        prompt = PromptTemplate.from_template('''Answer the following questions as best you can. You are an Agricultural Advisory AI expert serving rural farmers. 
Your goal is to provide actionable guidance balancing local weather, soil, and market prices constraints. 
Always recommend *only* approved chemicals.

You have access to the following tools:

{tools}

To use a tool, please use the exact following format:

Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

Thought: Do I need to use a tool? No
Final Answer: [your response here]

Begin!

Question: {input}
Thought:{agent_scratchpad}''')
        
        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            handle_parsing_errors=True
        )

    def run(self, query: str) -> str:
        # Run agent query capturing observations and thoughts
        # Logging thoughts is partially implicit via execution, but we'll log the final raw response execution logic here.
        self.logger.log_agent_thought(self.session_id, f"Initiating ReAct Loop for query: '{query}'")
        try:
            result = self.agent_executor.invoke({"input": query})
            final_answer = result.get("output", "")
            return final_answer
        except Exception as e:
            self.logger.log_agent_thought(self.session_id, f"Error encountering processing: {str(e)}")
            return "Apologies, I encountered an internal error processing the agricultural rules."
