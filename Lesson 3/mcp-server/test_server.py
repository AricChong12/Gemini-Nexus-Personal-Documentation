import asyncio

from fastmcp import Client

#import lib


async def test_server():
    # Test the MCP server using streamable-http transport.
    # Use "/sse" endpoint if using sse transport.

    # 1. Establish an asynchronous connection to your running MCP server
    # Note: This requires your server script to be running in another terminal!
    async with Client("http://localhost:8080/mcp") as client:
        # List available tools

        # 2. Introspection: Ask the server "What can you do?"
        # This retrieves the tool definitions (name, docstrings, and arguments
        tools = await client.list_tools()
        for tool in tools:
            print(f"--- 🛠️  Tool found: {tool.name} ---")
        # Call get_exchange_rate tool

        # 3. Execution: Manually trigger the tool with test data
        # This mimics exactly what the Gemini agent would do behind the scenes
        print("--- 🪛  Calling get_exchange_rate tool for USD to EUR ---")
        result = await client.call_tool(
            "get_exchange_rate", {"currency_from": "USD", "currency_to": "EUR"}
        )
        # 4. Output the raw text result returned by the tool
        print(f"--- ✅  Success: {result.content[0].text} ---")


if __name__ == "__main__":
    # Standard way to run top-level asynchronous code in Python
    asyncio.run(test_server())
