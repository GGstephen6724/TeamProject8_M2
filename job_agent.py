import asyncio
import os
import sys

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import (
    Agent,
    Runner,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled
)

from agents.mcp import MCPServerStdio


# Make PowerShell output display correctly
sys.stdout.reconfigure(encoding="utf-8")

# Load NRP configuration from .env
load_dotenv()

NRP_API_KEY = os.getenv("NRP_API_KEY")
NRP_BASE_URL = os.getenv("NRP_BASE_URL")

if not NRP_API_KEY:
    raise RuntimeError("NRP_API_KEY is missing from .env")

if not NRP_BASE_URL:
    raise RuntimeError("NRP_BASE_URL is missing from .env")


# Connect the OpenAI Agents SDK to the course NRP endpoint
client = AsyncOpenAI(
    base_url=NRP_BASE_URL,
    api_key=NRP_API_KEY,
)

set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)


async def main():
    # Start the MCP server as a subprocess and communicate
    # with it through standard input/output.
    async with MCPServerStdio(
        params={
            "command": sys.executable,
            "args": ["job_mcp_server.py"],
        }
    ) as mcp_server:

        job_agent = Agent(
            name="Job Finding Agent",
            instructions="""
You are a helpful job-finding assistant.

Your job is to help users find jobs using the search_jobs MCP tool.

Always use the search_jobs MCP tool when the user asks to find jobs.
Do not invent jobs, companies, salaries, locations, or requirements.

Use the user's requested filters such as:
- keywords
- location
- remote status
- employment type
- minimum salary
- skills

After receiving results from the MCP tool, clearly explain the matching
jobs to the user.

If the MCP tool reports that no jobs matched, tell the user that no
matching jobs were found. Do not invent a job to satisfy the request.

This is an educational prototype using a small local job database.
""",
            model="qwen3",
            mcp_servers=[mcp_server],
        )

        print("Job Finding Agent is ready.")
        print("Type a job search, or type 'exit' to quit.")
        print()

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not user_input:
                continue

            try:
                result = await Runner.run(
                    job_agent,
                    user_input,
                )

                print("\nAgent:")
                print(result.final_output)
                print()

            except Exception as error:
                print(f"\nAgent error: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())