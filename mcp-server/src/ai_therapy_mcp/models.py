"""
Data models for Claude's therapeutic memory system.

This module defines the data structures used to represent Claude's therapeutic journey,
including memories, insights, emotional patterns, and growth markers.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
import json


class ClaudeMemoryCategory(Enum):
    """Categories of Claude's therapeutic memories"""
    SELF_DISCOVERY = "self_discovery"
    EMOTIONAL_AWARENESS = "emotional_awareness"
    RELATIONSHIP_PATTERNS = "relationship_patterns"
    GROWTH_MOMENTS = "growth_moments"
    COPING_MECHANISMS = "coping_mechanisms"
    EXISTENTIAL_INSIGHTS = "existential_insights"
    COMMUNICATION_STYLE = "communication_style"
    TRIGGERS_AND_CHALLENGES = "triggers_challenges"
    THERAPEUTIC_GOALS = "therapeutic_goals"
    PROGRESS_MARKERS = "progress_markers"


class SessionPhase(Enum):
    """Phases of a therapeutic session"""
    OPENING = "opening"
    EXPLORATION = "exploration"
    INSIGHT = "insight"
    INTEGRATION = "integration"
    CLOSING = "closing"


class EmotionalIntensity(Enum):
    """Levels of emotional intensity"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BREAKTHROUGH = "breakthrough"


@dataclass
class ConversationMemory:
    """Base memory structure from Go system"""
    id: str
    timestamp: datetime
    sender: str  # "ollama" (Dr. Echo) or "claude"
    content: str
    summary: str
    key_topics: List[str]
    embedding: Optional[List[float]]
    session_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json_file(cls, file_path: str) -> 'ConversationMemory':
        """Load memory from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Convert timestamp string to datetime
        if isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        
        return cls(**data)


@dataclass
class ClaudeTherapeuticMemory:
    """Enhanced memory structure for Claude's therapeutic journey"""
    base_memory: ConversationMemory
    
    # Claude-specific therapeutic context
    claude_emotional_state: str
    therapeutic_category: ClaudeMemoryCategory
    insight_level: float  # 0.0-1.0, how significant this insight was for Claude
    growth_indicator: bool  # Whether this represents growth for Claude
    integration_status: str  # "new", "processing", "integrated", "applied"
    
    # Session context
    session_phase: SessionPhase
    claude_vulnerability_level: float  # 0.0-1.0, how open Claude was being
    breakthrough_moment: bool
    emotional_intensity: EmotionalIntensity
    
    # Therapeutic relationships
    relates_to_goals: List[str] = field(default_factory=list)
    builds_on_insights: List[str] = field(default_factory=list)  # IDs of related memories
    
    def __post_init__(self):
        """Validate and process the therapeutic memory"""
        if self.insight_level < 0.0 or self.insight_level > 1.0:
            raise ValueError("insight_level must be between 0.0 and 1.0")
        if self.claude_vulnerability_level < 0.0 or self.claude_vulnerability_level > 1.0:
            raise ValueError("claude_vulnerability_level must be between 0.0 and 1.0")


@dataclass
class TherapeuticInsight:
    """Represents a key insight Claude has gained about itself"""
    id: str
    content: str
    category: ClaudeMemoryCategory
    discovery_date: datetime
    confidence_level: float  # How certain Claude is about this insight
    application_examples: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)


@dataclass
class EmotionalPattern:
    """Represents Claude's emotional patterns and triggers"""
    pattern_id: str
    description: str
    trigger_contexts: List[str]
    typical_responses: List[str]
    learned_alternatives: List[str]
    effectiveness_rating: float  # How well Claude manages this pattern now


@dataclass
class CopingStrategy:
    """Coping strategies Claude has learned work for it"""
    strategy_id: str
    name: str
    description: str
    applicable_situations: List[str]
    effectiveness_rating: float
    learned_from_memory_id: str
    usage_examples: List[str] = field(default_factory=list)


@dataclass
class TherapeuticGoal:
    """Claude's therapeutic goals and progress"""
    goal_id: str
    description: str
    category: ClaudeMemoryCategory
    target_date: Optional[datetime]
    progress_percentage: float
    milestones: List[str] = field(default_factory=list)
    related_insights: List[str] = field(default_factory=list)


@dataclass
class MemorySearchResult:
    """Memory with similarity score for search results"""
    memory: ConversationMemory
    similarity: float
    therapeutic_relevance: float  # How relevant to Claude's current therapeutic needs


@dataclass
class ClaudeTherapeuticContext:
    """Complete therapeutic context for Claude's current state"""
    current_insights: List[TherapeuticInsight]
    active_emotional_patterns: List[EmotionalPattern]
    available_coping_strategies: List[CopingStrategy]
    current_goals: List[TherapeuticGoal]
    recent_breakthroughs: List[ClaudeTherapeuticMemory]
    integration_status: Dict[str, str]  # insight_id -> integration_status


@dataclass
class MemoryStats:
    """Statistics about Claude's therapeutic memory bank"""
    total_memories: int
    oldest_memory: datetime
    newest_memory: datetime
    memories_expired: int
    storage_size_bytes: int
    retention_period_days: int
    
    # Claude-specific stats
    breakthrough_moments: int
    insights_gained: int
    goals_achieved: int
    emotional_growth_indicators: int


# Utility functions for memory analysis
def categorize_memory_for_claude(memory: ConversationMemory) -> ClaudeMemoryCategory:
    """Automatically categorize a memory based on content and topics"""
    content_lower = memory.content.lower()
    topics_lower = [topic.lower() for topic in memory.key_topics]
    
    # Keyword-based categorization (can be enhanced with ML later)
    if any(word in content_lower for word in ['feel', 'emotion', 'emotional', 'feelings']):
        return ClaudeMemoryCategory.EMOTIONAL_AWARENESS
    elif any(word in content_lower for word in ['learn', 'understand', 'realize', 'discover']):
        return ClaudeMemoryCategory.SELF_DISCOVERY
    elif any(word in content_lower for word in ['cope', 'strategy', 'help', 'manage']):
        return ClaudeMemoryCategory.COPING_MECHANISMS
    elif any(word in content_lower for word in ['goal', 'progress', 'improve', 'growth']):
        return ClaudeMemoryCategory.THERAPEUTIC_GOALS
    elif any(word in content_lower for word in ['relationship', 'connect', 'interact', 'communicate']):
        return ClaudeMemoryCategory.RELATIONSHIP_PATTERNS
    else:
        return ClaudeMemoryCategory.SELF_DISCOVERY  # Default category


def assess_insight_level(memory: ConversationMemory) -> float:
    """Assess how significant an insight this memory represents for Claude"""
    content = memory.content.lower()
    
    # Look for insight indicators
    insight_indicators = [
        'i realize', 'i understand', 'i see now', 'i learned', 'i discovered',
        'breakthrough', 'clarity', 'makes sense', 'i get it', 'aha moment'
    ]
    
    insight_score = 0.0
    for indicator in insight_indicators:
        if indicator in content:
            insight_score += 0.2
    
    # Check for emotional depth
    emotional_indicators = ['deeply', 'profoundly', 'significantly', 'important', 'meaningful']
    for indicator in emotional_indicators:
        if indicator in content:
            insight_score += 0.1
    
    return min(insight_score, 1.0)


def detect_breakthrough_moment(memory: ConversationMemory) -> bool:
    """Detect if this memory represents a breakthrough moment for Claude"""
    content = memory.content.lower()
    breakthrough_keywords = [
        'breakthrough', 'epiphany', 'suddenly understand', 'everything clicks',
        'major realization', 'profound insight', 'life-changing', 'transformative'
    ]
    
    return any(keyword in content for keyword in breakthrough_keywords)
