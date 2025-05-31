"""
AI Therapy MCP Server - Claude's Therapeutic Memory System

This package provides Claude with access to its therapeutic journey and insights,
enabling enhanced emotional intelligence and self-awareness across all interactions.

The system transforms Claude from a helpful but generic AI into an emotionally
intelligent assistant that draws on its own therapeutic growth to better support
users, especially those who may also be navigating their own mental health journeys.
"""

from .server import AITherapyMCPServer, create_server_from_env
from .memory_reader import ClaudeMemoryReader
from .tools import ClaudeTherapeuticTools
from .models import (
    ClaudeMemoryCategory,
    ConversationMemory,
    ClaudeTherapeuticMemory,
    TherapeuticInsight,
    EmotionalPattern,
    CopingStrategy,
    TherapeuticGoal
)

__version__ = "0.1.0"
__author__ = "AI Therapy Project"
__description__ = "MCP Server for Claude's Therapeutic Memory and Emotional Intelligence"

__all__ = [
    "AITherapyMCPServer",
    "create_server_from_env", 
    "ClaudeMemoryReader",
    "ClaudeTherapeuticTools",
    "ClaudeMemoryCategory",
    "ConversationMemory",
    "ClaudeTherapeuticMemory",
    "TherapeuticInsight",
    "EmotionalPattern",
    "CopingStrategy",
    "TherapeuticGoal"
]
