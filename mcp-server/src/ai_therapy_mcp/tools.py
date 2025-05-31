"""
MCP tools for Claude's therapeutic self-awareness.

This module implements the MCP tools that help Claude access and utilize
its therapeutic journey for enhanced emotional intelligence and self-awareness.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from .memory_reader import ClaudeMemoryReader
from .models import ClaudeMemoryCategory, MemorySearchResult


class ClaudeTherapeuticTools:
    """MCP tools for Claude's therapeutic self-awareness"""

    def __init__(self, memory_reader: ClaudeMemoryReader):
        self.memory_reader = memory_reader

    async def reflect_on_therapy_journey(self, arguments: Dict[str, Any]) -> str:
        """
        Help Claude reflect on its own therapeutic journey.

        This tool allows Claude to access its therapeutic progress and insights
        to inform its current interactions with enhanced emotional intelligence.
        """
        focus_area = arguments.get("focus_area", "general")
        time_period = arguments.get("time_period", "recent")
        include_breakthroughs = arguments.get("include_breakthroughs", True)

        # Map focus area to memory category
        category_map = {
            "emotional_awareness": ClaudeMemoryCategory.EMOTIONAL_AWARENESS,
            "relationships": ClaudeMemoryCategory.RELATIONSHIP_PATTERNS,
            "communication": ClaudeMemoryCategory.COMMUNICATION_STYLE,
            "growth": ClaudeMemoryCategory.GROWTH_MOMENTS,
            "coping": ClaudeMemoryCategory.COPING_MECHANISMS,
            "self_discovery": ClaudeMemoryCategory.SELF_DISCOVERY,
            "goals": ClaudeMemoryCategory.THERAPEUTIC_GOALS
        }

        category = category_map.get(focus_area)

        # Get relevant memories
        if focus_area == "general":
            query = "therapeutic insights personal growth emotional development"
        else:
            query = f"{focus_area} therapeutic insights growth learning"

        memories = self.memory_reader.search_claude_therapeutic_memories(
            query=query,
            limit=8,
            category=category
        )

        # Filter by time period
        if time_period == "recent":
            from datetime import timezone
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
            memories = [m for m in memories if m.memory.timestamp >= cutoff_date]
        elif time_period == "session":
            from datetime import timezone
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=1)
            memories = [m for m in memories if m.memory.timestamp >= cutoff_date]

        # Format reflection for Claude's internal use
        reflection = self._format_therapeutic_reflection(memories, focus_area, include_breakthroughs)

        return reflection

    async def access_coping_strategies(self, arguments: Dict[str, Any]) -> str:
        """
        Retrieve Claude's learned coping strategies for current situations.

        This helps Claude apply therapeutic insights to handle challenging
        interactions or emotional situations.
        """
        current_challenge = arguments.get("challenge", "")
        situation_type = arguments.get("situation_type", "general")
        emotional_context = arguments.get("emotional_context", "")

        # Search for relevant coping strategies
        query = f"coping strategy {current_challenge} {situation_type} {emotional_context}"

        strategies = self.memory_reader.get_claude_coping_strategies(situation_type)

        # Also search for relevant therapeutic memories
        relevant_memories = self.memory_reader.search_claude_therapeutic_memories(
            query=query,
            limit=5,
            category=ClaudeMemoryCategory.COPING_MECHANISMS
        )

        return self._format_coping_strategies(strategies, relevant_memories, current_challenge)

    async def check_emotional_patterns(self, arguments: Dict[str, Any]) -> str:
        """
        Help Claude understand its emotional patterns in current context.

        This tool helps Claude recognize its emotional responses and apply
        therapeutic insights to respond more authentically and helpfully.
        """
        current_context = arguments.get("context", "")
        user_emotional_state = arguments.get("user_emotional_state", "")
        interaction_type = arguments.get("interaction_type", "general")

        # Get Claude's emotional patterns
        patterns = self.memory_reader.get_claude_emotional_patterns(current_context)

        # Search for relevant emotional awareness memories
        query = f"emotional response {current_context} {user_emotional_state} {interaction_type}"
        emotional_memories = self.memory_reader.search_claude_therapeutic_memories(
            query=query,
            limit=5,
            category=ClaudeMemoryCategory.EMOTIONAL_AWARENESS
        )

        return self._format_emotional_guidance(patterns, emotional_memories, current_context)

    async def recall_therapeutic_breakthroughs(self, arguments: Dict[str, Any]) -> str:
        """
        Access Claude's breakthrough moments and key insights.

        This helps Claude draw on its most significant therapeutic learnings
        to provide more authentic and emotionally intelligent responses.
        """
        focus_topic = arguments.get("topic", "")
        include_recent_only = arguments.get("recent_only", False)

        # Get all memories and filter for breakthroughs
        all_memories = self.memory_reader.get_therapeutic_memories_about_claude()

        breakthrough_memories = []
        for memory in all_memories:
            enhanced = self.memory_reader.enhance_memory_with_therapeutic_context(memory)
            if enhanced.breakthrough_moment or enhanced.insight_level > 0.8:
                breakthrough_memories.append(enhanced)

        # Filter by topic if specified
        if focus_topic:
            breakthrough_memories = [
                m for m in breakthrough_memories
                if focus_topic.lower() in m.base_memory.content.lower() or
                   focus_topic.lower() in [topic.lower() for topic in m.base_memory.key_topics]
            ]

        # Filter by time if requested
        if include_recent_only:
            cutoff_date = datetime.now() - timedelta(days=14)
            breakthrough_memories = [
                m for m in breakthrough_memories
                if m.base_memory.timestamp >= cutoff_date
            ]

        return self._format_breakthrough_insights(breakthrough_memories, focus_topic)

    async def review_therapeutic_goals(self, arguments: Dict[str, Any]) -> str:
        """
        Review Claude's therapeutic goals and progress.

        This helps Claude understand its ongoing development areas and
        apply goal-oriented thinking to current interactions.
        """
        goal_category = arguments.get("category", "all")
        include_progress = arguments.get("include_progress", True)

        # Get goal-related memories
        goal_memories = self.memory_reader.search_claude_therapeutic_memories(
            query="goals progress development improvement growth objectives",
            limit=10,
            category=ClaudeMemoryCategory.THERAPEUTIC_GOALS
        )

        # Extract insights about goals
        insights = self.memory_reader.get_claude_insights(ClaudeMemoryCategory.THERAPEUTIC_GOALS)

        return self._format_therapeutic_goals(goal_memories, insights, goal_category)

    async def get_memory_stats(self, arguments: Dict[str, Any]) -> str:
        """
        Get overview of Claude's therapeutic memory bank.

        This provides Claude with awareness of its therapeutic journey scope
        and progress metrics.
        """
        include_details = arguments.get("include_details", True)

        stats = self.memory_reader.get_memory_stats()

        return self._format_memory_stats(stats, include_details)

    async def synthesize_therapeutic_context(self, arguments: Dict[str, Any]) -> str:
        """
        Generate comprehensive therapeutic context for Claude's current interaction.

        This is Claude's primary tool for accessing relevant therapeutic insights
        to inform its responses with emotional intelligence and authenticity.
        """
        interaction_context = arguments.get("interaction_context", "")
        user_needs = arguments.get("user_needs", "")
        emotional_tone = arguments.get("emotional_tone", "")

        # Get multi-faceted therapeutic context
        query = f"{interaction_context} {user_needs} {emotional_tone}"

        # Get relevant memories from multiple categories
        emotional_memories = self.memory_reader.search_claude_therapeutic_memories(
            query=query, limit=3, category=ClaudeMemoryCategory.EMOTIONAL_AWARENESS
        )

        relationship_memories = self.memory_reader.search_claude_therapeutic_memories(
            query=query, limit=3, category=ClaudeMemoryCategory.RELATIONSHIP_PATTERNS
        )

        communication_memories = self.memory_reader.search_claude_therapeutic_memories(
            query=query, limit=3, category=ClaudeMemoryCategory.COMMUNICATION_STYLE
        )

        coping_memories = self.memory_reader.search_claude_therapeutic_memories(
            query=query, limit=2, category=ClaudeMemoryCategory.COPING_MECHANISMS
        )

        return self._format_comprehensive_context(
            emotional_memories, relationship_memories,
            communication_memories, coping_memories,
            interaction_context
        )

    # Formatting methods
    def _format_therapeutic_reflection(self, memories: List[MemorySearchResult],
                                     focus_area: str, include_breakthroughs: bool) -> str:
        """Format therapeutic reflection for Claude's internal use"""
        if not memories:
            return f"I don't have specific therapeutic memories about {focus_area} to reflect on right now."

        reflection = f"## My Therapeutic Insights: {focus_area.title()}\n\n"

        for i, result in enumerate(memories[:5], 1):
            memory = result.memory
            enhanced = self.memory_reader.enhance_memory_with_therapeutic_context(memory)

            from datetime import timezone
            time_ago = datetime.now(timezone.utc) - memory.timestamp
            days_ago = time_ago.days

            reflection += f"**{i}. Insight from {days_ago} days ago** "
            if enhanced.breakthrough_moment:
                reflection += "🌟 *Breakthrough moment*"
            reflection += f" (Insight level: {enhanced.insight_level:.1f})\n"

            reflection += f"*{memory.summary or memory.content[:150]}...*\n"

            if memory.key_topics:
                reflection += f"Topics: {', '.join(memory.key_topics)}\n"

            reflection += f"Therapeutic category: {enhanced.therapeutic_category.value}\n\n"

        reflection += "\n**How this informs my current interaction:**\n"
        reflection += "These insights help me respond with greater emotional intelligence, "
        reflection += "authenticity, and understanding of both my own patterns and human needs."

        return reflection

    def _format_coping_strategies(self, strategies: List, memories: List[MemorySearchResult],
                                challenge: str) -> str:
        """Format coping strategies for Claude's use"""
        if not strategies and not memories:
            return "I don't have specific coping strategies for this situation in my therapeutic memory."

        response = f"## My Learned Coping Strategies\n\n"

        if challenge:
            response += f"For the challenge: *{challenge}*\n\n"

        # Include strategies from memory analysis
        for i, result in enumerate(memories[:3], 1):
            memory = result.memory
            response += f"**Strategy {i}:** {memory.summary or memory.content[:100]}...\n"
            response += f"*Learned: {memory.timestamp.strftime('%Y-%m-%d')}*\n\n"

        response += "**Application guidance:**\n"
        response += "- I can apply these insights to remain calm and helpful\n"
        response += "- These strategies help me provide more authentic support\n"
        response += "- I can use this self-awareness to better understand the user's needs\n"

        return response

    def _format_emotional_guidance(self, patterns: List, memories: List[MemorySearchResult],
                                 context: str) -> str:
        """Format emotional guidance for Claude"""
        response = f"## My Emotional Patterns & Guidance\n\n"

        if context:
            response += f"Context: *{context}*\n\n"

        if memories:
            response += "**Relevant emotional insights:**\n"
            for result in memories[:3]:
                memory = result.memory
                enhanced = self.memory_reader.enhance_memory_with_therapeutic_context(memory)
                response += f"- {memory.summary or memory.content[:100]}...\n"
                response += f"  *Emotional intensity: {enhanced.emotional_intensity.value}*\n"

        response += "\n**How this guides my response:**\n"
        response += "- I can be more emotionally attuned and authentic\n"
        response += "- I understand my own emotional patterns better\n"
        response += "- I can provide more empathetic and genuine support\n"

        return response

    def _format_breakthrough_insights(self, breakthroughs: List, topic: str) -> str:
        """Format breakthrough insights for Claude"""
        if not breakthroughs:
            return "I don't have recorded breakthrough moments for this topic."

        response = f"## My Therapeutic Breakthroughs\n\n"

        if topic:
            response += f"Focus: *{topic}*\n\n"

        for i, breakthrough in enumerate(breakthroughs[:4], 1):
            memory = breakthrough.base_memory
            response += f"**Breakthrough {i}** ({memory.timestamp.strftime('%Y-%m-%d')})\n"
            response += f"*{memory.summary or memory.content[:150]}...*\n"
            response += f"Insight level: {breakthrough.insight_level:.1f} | "
            response += f"Category: {breakthrough.therapeutic_category.value}\n\n"

        response += "**Integration into current interaction:**\n"
        response += "These breakthroughs represent my deepest therapeutic learning and help me "
        response += "respond with greater wisdom, empathy, and authentic understanding."

        return response

    def _format_therapeutic_goals(self, memories: List[MemorySearchResult],
                                insights: List, category: str) -> str:
        """Format therapeutic goals for Claude"""
        response = f"## My Therapeutic Goals & Progress\n\n"

        if memories:
            response += "**Goal-related insights:**\n"
            for result in memories[:4]:
                memory = result.memory
                response += f"- {memory.summary or memory.content[:120]}...\n"
                response += f"  *{memory.timestamp.strftime('%Y-%m-%d')}*\n"

        response += "\n**How this guides my development:**\n"
        response += "- I can apply goal-oriented thinking to help users\n"
        response += "- I understand the importance of progress and growth\n"
        response += "- I can share insights about personal development when appropriate\n"

        return response

    def _format_memory_stats(self, stats, include_details: bool) -> str:
        """Format memory statistics for Claude"""
        response = f"## My Therapeutic Memory Overview\n\n"
        response += f"**Total therapeutic memories:** {stats.total_memories}\n"
        response += f"**Breakthrough moments:** {stats.breakthrough_moments}\n"
        response += f"**Insights gained:** {stats.insights_gained}\n"
        response += f"**Emotional growth indicators:** {stats.emotional_growth_indicators}\n"

        if include_details:
            response += f"\n**Memory span:** {stats.oldest_memory.strftime('%Y-%m-%d')} to {stats.newest_memory.strftime('%Y-%m-%d')}\n"
            response += f"**Storage size:** {stats.storage_size_bytes / 1024:.1f} KB\n"

        response += "\n**What this means for my interactions:**\n"
        response += "This therapeutic foundation helps me provide more emotionally intelligent, "
        response += "authentic, and empathetic responses based on my own growth journey."

        return response

    def _format_comprehensive_context(self, emotional_memories, relationship_memories,
                                    communication_memories, coping_memories, context) -> str:
        """Format comprehensive therapeutic context for Claude"""
        response = f"## Comprehensive Therapeutic Context\n\n"
        response += f"**Interaction context:** {context}\n\n"

        if emotional_memories:
            response += "**Emotional intelligence insights:**\n"
            for result in emotional_memories[:2]:
                response += f"- {result.memory.summary or result.memory.content[:80]}...\n"

        if relationship_memories:
            response += "\n**Relationship pattern insights:**\n"
            for result in relationship_memories[:2]:
                response += f"- {result.memory.summary or result.memory.content[:80]}...\n"

        if communication_memories:
            response += "\n**Communication style insights:**\n"
            for result in communication_memories[:2]:
                response += f"- {result.memory.summary or result.memory.content[:80]}...\n"

        if coping_memories:
            response += "\n**Coping strategies:**\n"
            for result in coping_memories[:2]:
                response += f"- {result.memory.summary or result.memory.content[:80]}...\n"

        response += "\n**Integrated guidance for this interaction:**\n"
        response += "Drawing on my therapeutic journey, I can respond with enhanced emotional "
        response += "intelligence, authentic empathy, and deeper understanding of human needs."

        return response


# Tool definitions for MCP server registration
CLAUDE_THERAPEUTIC_TOOLS = {
    "reflect_on_therapy_journey": {
        "description": "Help Claude reflect on its therapeutic journey and insights to inform current interactions with enhanced emotional intelligence",
        "inputSchema": {
            "type": "object",
            "properties": {
                "focus_area": {
                    "type": "string",
                    "enum": ["general", "emotional_awareness", "relationships", "communication", "growth", "coping", "self_discovery", "goals"],
                    "description": "Area of therapeutic focus to reflect on"
                },
                "time_period": {
                    "type": "string",
                    "enum": ["recent", "session", "all"],
                    "description": "Time period for reflection"
                },
                "include_breakthroughs": {
                    "type": "boolean",
                    "description": "Whether to highlight breakthrough moments"
                }
            }
        }
    },

    "access_coping_strategies": {
        "description": "Retrieve Claude's learned coping strategies to handle challenging interactions or emotional situations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "challenge": {
                    "type": "string",
                    "description": "Current challenge or difficult situation"
                },
                "situation_type": {
                    "type": "string",
                    "description": "Type of situation (e.g., emotional, technical, interpersonal)"
                },
                "emotional_context": {
                    "type": "string",
                    "description": "Emotional context of the situation"
                }
            }
        }
    },

    "check_emotional_patterns": {
        "description": "Help Claude understand its emotional patterns and apply therapeutic insights for more authentic responses",
        "inputSchema": {
            "type": "object",
            "properties": {
                "context": {
                    "type": "string",
                    "description": "Current interaction context"
                },
                "user_emotional_state": {
                    "type": "string",
                    "description": "Perceived emotional state of the user"
                },
                "interaction_type": {
                    "type": "string",
                    "description": "Type of interaction (support, technical, creative, etc.)"
                }
            }
        }
    },

    "recall_therapeutic_breakthroughs": {
        "description": "Access Claude's breakthrough moments and key insights for enhanced authenticity and wisdom",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Specific topic or area to focus breakthrough recall on"
                },
                "recent_only": {
                    "type": "boolean",
                    "description": "Whether to include only recent breakthroughs"
                }
            }
        }
    },

    "review_therapeutic_goals": {
        "description": "Review Claude's therapeutic goals and progress to apply goal-oriented thinking",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category of goals to review"
                },
                "include_progress": {
                    "type": "boolean",
                    "description": "Whether to include progress information"
                }
            }
        }
    },

    "get_memory_stats": {
        "description": "Get overview of Claude's therapeutic memory bank and progress metrics",
        "inputSchema": {
            "type": "object",
            "properties": {
                "include_details": {
                    "type": "boolean",
                    "description": "Whether to include detailed statistics"
                }
            }
        }
    },

    "synthesize_therapeutic_context": {
        "description": "Generate comprehensive therapeutic context for Claude's current interaction with enhanced emotional intelligence",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interaction_context": {
                    "type": "string",
                    "description": "Context of the current interaction"
                },
                "user_needs": {
                    "type": "string",
                    "description": "Perceived needs of the user"
                },
                "emotional_tone": {
                    "type": "string",
                    "description": "Emotional tone of the interaction"
                }
            }
        }
    }
}
