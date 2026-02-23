import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            tools = await session.list_tools()
            print("TOOLS:", tools)

            result = await session.call_tool(
                "create_task",
                {
                    "title": "Test",
                    "desc": "My first task",
                    "deadline": "2026-03-01"
                }
            )

            print("RESULT:", result)

asyncio.run(main())