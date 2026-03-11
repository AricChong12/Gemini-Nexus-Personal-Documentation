import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

#import lib


# 1. Create a specialized logger for this specific module
# __name__ ensures the log shows exactly which file the message came from
logger = logging.getLogger(__name__)

# 2. Set the global 'rules' for how logs should look and what priority to show
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
# Example output: [INFO]: Server started
# Ignore DEBUG logs; show INFO and above

# 3. Look for a .env file and load its key-value pairs into the system environment
load_dotenv()

# 1. Define the 'System Instruction' (The Agent's Identity)
# This string acts as a hard boundary for the AI's behavior.
SYSTEM_INSTRUCTION = (
    "You are a specialized assistant for currency conversions. "
    "Your sole purpose is to use the 'get_exchange_rate' tool to answer questions about currency exchange rates. "
    "If the user asks about anything other than currency conversion or exchange rates, "
    "politely state that you cannot help with that topic and can only assist with currency-related queries. "
    "Do not attempt to answer unrelated questions or use tools for other purposes."
)

# 2. Informative logs to track the initialization process
# These will appear in your console prefixed with [INFO] based on your previous config.
logger.info("--- 🔧 Loading MCP tools from MCP Server... ---")
logger.info("--- 🤖 Creating ADK Currency Agent... ---")

# 1. Initialize the AI Agent
root_agent = LlmAgent(
    model="gemini-2.5-flash",   # Specifies the "brain" (Gemini 2.5 Flash)
    name="currency_agent",      # Internal identifier for the agent
    description="An agent that can help with currency conversions",
    instruction=SYSTEM_INSTRUCTION,    # The guardrails we defined earlier
    tools=[
        # 2. Connect the Agent to external capabilities via MCP
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                # Use an environment variable for the URL, defaulting to localhost
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
            )
        )
    ],
)

# Make the agent A2A-compatible
# 3. Transform the agent into a service (Agent-to-Agent/A2A)
# This wraps the agent in an API layer listening on port 10000
a2a_app = to_a2a(root_agent, port=10000)
