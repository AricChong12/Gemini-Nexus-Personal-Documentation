import asyncio
import logging
import os

import httpx
from fastmcp import FastMCP
#import lib

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# 1. Initialize the FastMCP server instance
mcp = FastMCP("Currency MCP Server 💵")

# 2. Register a 'Tool' that the AI Agent can discover and use
@mcp.tool()
def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Use this to get current exchange rate.

    Args:
        currency_from: The currency to convert from (e.g., "USD").
        currency_to: The currency to convert to (e.g., "EUR").
        currency_date: The date for the exchange rate or "latest". Defaults to "latest".

    Returns:
        A dictionary containing the exchange rate data, or an error message if the request fails.
    """
    logger.info(
        f"--- 🛠️ Tool: get_exchange_rate called for converting {currency_from} to {currency_to} ---"
    )
    try:
        # 3. Perform the actual HTTP request to the Frankfurter API
        response = httpx.get(
            f"https://api.frankfurter.app/{currency_date}",
            params={"from": currency_from, "to": currency_to},
        )
        response.raise_for_status() # Check if the request actually worked

        data = response.json()

        # Validation: Ensure the API returned the expected 'rates' field
        if "rates" not in data:
            logger.error(f"❌ rates not found in response: {data}")
            return {"error": "Invalid API response format."}
        logger.info(f"✅ API response: {data}")
        return data  # Send the data back to the AI Agent
    except httpx.HTTPError as e:
        logger.error(f"❌ API request failed: {e}")
        return {"error": f"API request failed: {e}"}
    except ValueError:
        logger.error("❌ Invalid JSON response from API")
        return {"error": "Invalid JSON response from API."}

# 4. Entry point to run the server
if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.

    # Start the server using 'http' transport on port 8080 (or your env port)
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",  # Allows external connections (important for Docker/Cloud)
            port=os.getenv("PORT", 8080),
        )
    )
