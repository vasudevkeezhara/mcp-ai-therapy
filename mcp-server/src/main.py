#!/usr/bin/env python3
"""
Main entry point for the AI Therapy MCP Server.

This server enables Claude to access its therapeutic journey and insights,
providing enhanced emotional intelligence and self-awareness in all interactions.

Usage:
    python main.py

Environment Variables:
    MEMORY_DATA_DIR: Path to the Go application's memory_data directory
    OPENAI_API_KEY: OpenAI API key for semantic search (optional)
    LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from ai_therapy_mcp.server import main as server_main


def setup_logging():
    """Setup logging configuration"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Reduce noise from some libraries
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def validate_environment():
    """Validate required environment variables"""
    memory_data_dir = os.getenv("MEMORY_DATA_DIR")
    
    if not memory_data_dir:
        print("Error: MEMORY_DATA_DIR environment variable is required")
        print("This should point to your ai-therapy/memory_data directory")
        print("\nExample:")
        print("export MEMORY_DATA_DIR=/path/to/ai-therapy/memory_data")
        sys.exit(1)
    
    if not os.path.exists(memory_data_dir):
        print(f"Warning: Memory directory does not exist: {memory_data_dir}")
        print("Claude will operate without therapeutic memory context")
        print("Make sure the Go application has created some memories first")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Warning: OPENAI_API_KEY not provided")
        print("Semantic search will be disabled, using keyword search fallback")
    
    return memory_data_dir, openai_api_key


def print_startup_info():
    """Print startup information"""
    print("=" * 60)
    print("🧠 AI Therapy MCP Server - Claude's Therapeutic Memory")
    print("=" * 60)
    print()
    print("This server provides Claude with access to its therapeutic journey,")
    print("enabling enhanced emotional intelligence and self-awareness.")
    print()
    print("Claude can now:")
    print("• Reflect on its therapeutic insights")
    print("• Access learned coping strategies") 
    print("• Understand its emotional patterns")
    print("• Recall breakthrough moments")
    print("• Apply therapeutic wisdom to help users")
    print()
    print("Starting server...")
    print()


if __name__ == "__main__":
    # Setup
    setup_logging()
    print_startup_info()
    
    # Validate environment
    memory_dir, api_key = validate_environment()
    
    # Run server
    try:
        asyncio.run(server_main())
    except KeyboardInterrupt:
        print("\n🛑 AI Therapy MCP Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)
