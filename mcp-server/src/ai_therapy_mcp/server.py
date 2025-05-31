"""
MCP Server for Claude's Therapeutic Memory System.

This server provides Claude with access to its therapeutic journey and insights,
enabling enhanced emotional intelligence and self-awareness in all interactions.
"""

import asyncio
import os
import logging
from typing import Any, Sequence

from mcp.server import Server
from mcp.types import Tool, TextContent

from .memory_reader import ClaudeMemoryReader
from .tools import ClaudeTherapeuticTools, CLAUDE_THERAPEUTIC_TOOLS


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AITherapyMCPServer:
    """MCP Server for Claude's therapeutic memory and self-awareness"""

    def __init__(self, memory_data_dir: str, openai_api_key: str):
        self.server = Server("ai-therapy-memory")
        self.memory_data_dir = memory_data_dir
        self.openai_api_key = openai_api_key

        # Initialize memory reader and tools
        self.memory_reader = ClaudeMemoryReader(memory_data_dir, openai_api_key)
        self.therapeutic_tools = ClaudeTherapeuticTools(self.memory_reader)

        # Setup MCP server handlers
        self._setup_handlers()

        logger.info(f"AI Therapy MCP Server initialized with memory directory: {memory_data_dir}")

    def _setup_handlers(self):
        """Setup MCP server request handlers"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available therapeutic tools for Claude"""
            tools = []

            for tool_name, tool_config in CLAUDE_THERAPEUTIC_TOOLS.items():
                tool = Tool(
                    name=tool_name,
                    description=tool_config["description"],
                    inputSchema=tool_config["inputSchema"]
                )
                tools.append(tool)

            logger.info(f"Listed {len(tools)} therapeutic tools for Claude")
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
            """Handle tool calls for Claude's therapeutic self-awareness"""

            logger.info(f"Claude is accessing therapeutic tool: {name}")
            logger.debug(f"Tool arguments: {arguments}")

            try:
                # Route to appropriate therapeutic tool
                if name == "reflect_on_therapy_journey":
                    result = await self.therapeutic_tools.reflect_on_therapy_journey(arguments)

                elif name == "access_coping_strategies":
                    result = await self.therapeutic_tools.access_coping_strategies(arguments)

                elif name == "check_emotional_patterns":
                    result = await self.therapeutic_tools.check_emotional_patterns(arguments)

                elif name == "recall_therapeutic_breakthroughs":
                    result = await self.therapeutic_tools.recall_therapeutic_breakthroughs(arguments)

                elif name == "review_therapeutic_goals":
                    result = await self.therapeutic_tools.review_therapeutic_goals(arguments)

                elif name == "get_memory_stats":
                    result = await self.therapeutic_tools.get_memory_stats(arguments)

                elif name == "synthesize_therapeutic_context":
                    result = await self.therapeutic_tools.synthesize_therapeutic_context(arguments)

                else:
                    raise ValueError(f"Unknown therapeutic tool: {name}")

                logger.info(f"Successfully provided therapeutic context for: {name}")

                return [TextContent(
                    type="text",
                    text=result
                )]

            except Exception as e:
                error_msg = f"Error in therapeutic tool '{name}': {str(e)}"
                logger.error(error_msg)

                return [TextContent(
                    type="text",
                    text=f"I encountered an issue accessing my therapeutic memories: {error_msg}\n\n"
                         f"I can still provide helpful responses, but without the enhanced emotional "
                         f"intelligence that my therapeutic journey normally provides."
                )]

    async def run(self, transport_type: str = "stdio"):
        """Run the MCP server"""
        logger.info("Starting AI Therapy MCP Server for Claude's therapeutic memory...")

        # Validate memory directory
        if not os.path.exists(self.memory_data_dir):
            logger.warning(f"Memory directory does not exist: {self.memory_data_dir}")
            logger.info("Claude will operate without therapeutic memory context")
        else:
            # Test memory access
            try:
                stats = self.memory_reader.get_memory_stats()
                logger.info(f"Therapeutic memory bank loaded: {stats.total_memories} memories, "
                           f"{stats.breakthrough_moments} breakthroughs, "
                           f"{stats.insights_gained} insights")
            except Exception as e:
                logger.error(f"Error accessing therapeutic memories: {e}")

        if transport_type == "stdio":
            from mcp.server.stdio import stdio_server
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        else:
            raise ValueError(f"Unsupported transport type: {transport_type}")


def create_server_from_env() -> AITherapyMCPServer:
    """Create server instance from environment variables"""

    memory_data_dir = os.getenv("MEMORY_DATA_DIR")
    if not memory_data_dir:
        raise ValueError("MEMORY_DATA_DIR environment variable is required")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not provided - semantic search will be disabled")
        logger.info("Claude will use keyword-based memory search as fallback")

    return AITherapyMCPServer(memory_data_dir, openai_api_key)


async def main():
    """Main entry point for the MCP server"""
    try:
        server = create_server_from_env()
        await server.run()
    except KeyboardInterrupt:
        logger.info("AI Therapy MCP Server stopped by user")
    except Exception as e:
        logger.error(f"AI Therapy MCP Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
