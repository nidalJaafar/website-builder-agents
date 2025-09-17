from langchain_mcp_adapters.client import MultiServerMCPClient

from website_builder.config import PROJECT_WORKSPACE


async def mcp_file_system_tools():
    client = MultiServerMCPClient({
        "filesystem": {
            "command": "npx",
            "args": [
                "-y", "@modelcontextprotocol/server-filesystem",
                PROJECT_WORKSPACE
            ],
            "transport": "stdio"
        }
    })
    return await client.get_tools()
