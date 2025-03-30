import asyncio
from dataclasses import dataclass, field
from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",
    args=["./mcp_server.py"],
    env=None,
)

@dataclass
class Chat:
    messages: List[SystemMessage | HumanMessage | AIMessage] = field(default_factory=list)
    
    system_prompt: str = """You are a master PostgreSQL assistant. 
    Your job is to use the tools at your disposal to execute SQL queries and provide the results to the user."""

    async def setup_agent(self, session: ClientSession):
        # Get available tools from MCP
        response = await session.list_tools()
        
        async def call_mcp_tool(tool_name: str, sql: str):
            result = await session.call_tool("query_data", {"sql": sql})
            return result.content[0].text

        tools = [
            Tool(
                name="query_data",
                description="Execute SQL queries safely",
                func=lambda *_, **__: None,  # Dummy sync function
                coroutine=lambda sql: call_mcp_tool("query_data", sql)
            )
        ]

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Initialize OpenAI model through LangChain
        model = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0
        )

        # Create agent with OpenAI tools
        agent = create_openai_tools_agent(model, tools, prompt)
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True
        )

    async def process_query(self, query: str) -> None:
        # Run the agent
        response = await self.agent_executor.ainvoke(
            {
                "input": query,
                "chat_history": self.messages
            }
        )
        
        # Store messages for chat history
        self.messages.append(HumanMessage(content=query))
        self.messages.append(AIMessage(content=response["output"]))
        
        print(response["output"])

    async def chat_loop(self, session: ClientSession):
        # Setup agent first
        await self.setup_agent(session)
        
        while True:
            query = input("\nQuery: ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            await self.process_query(query)

    async def run(self):
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                await self.chat_loop(session)

chat = Chat()
asyncio.run(chat.run())