"""
Memory reader interface for Claude's therapeutic journey.

This module provides the interface to read and analyze the Go-based memory system
from Claude's therapeutic perspective, focusing on Claude's growth and insights.
"""

import json
import os
import glob
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import numpy as np
from openai import OpenAI

from .models import (
    ConversationMemory, ClaudeTherapeuticMemory, MemorySearchResult,
    TherapeuticInsight, EmotionalPattern, CopingStrategy, TherapeuticGoal,
    ClaudeTherapeuticContext, MemoryStats, ClaudeMemoryCategory,
    categorize_memory_for_claude, assess_insight_level, detect_breakthrough_moment,
    SessionPhase, EmotionalIntensity
)


class ClaudeMemoryReader:
    """Interface to read Go-based memory system from Claude's therapeutic perspective"""
    
    def __init__(self, memory_data_dir: str, openai_api_key: str):
        self.memory_data_dir = memory_data_dir
        self.openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
        self._memory_cache = None
        self._cache_timestamp = None
        self.cache_duration = timedelta(minutes=5)  # Cache for 5 minutes
    
    def _load_memories_from_disk(self) -> List[ConversationMemory]:
        """Load all memory JSON files from the Go system"""
        if not os.path.exists(self.memory_data_dir):
            return []
        
        memories = []
        json_files = glob.glob(os.path.join(self.memory_data_dir, "*.json"))
        
        for file_path in json_files:
            try:
                memory = ConversationMemory.from_json_file(file_path)
                memories.append(memory)
            except Exception as e:
                print(f"Warning: Could not load memory from {file_path}: {e}")
                continue
        
        # Sort by timestamp (newest first)
        memories.sort(key=lambda m: m.timestamp, reverse=True)
        return memories
    
    def load_all_memories(self) -> List[ConversationMemory]:
        """Load all memories with caching"""
        now = datetime.now()
        
        # Use cache if it's fresh
        if (self._memory_cache is not None and 
            self._cache_timestamp is not None and 
            now - self._cache_timestamp < self.cache_duration):
            return self._memory_cache
        
        # Reload from disk
        self._memory_cache = self._load_memories_from_disk()
        self._cache_timestamp = now
        return self._memory_cache
    
    def get_claude_memories_only(self) -> List[ConversationMemory]:
        """Get only memories where Claude was speaking (Claude's own expressions)"""
        all_memories = self.load_all_memories()
        return [memory for memory in all_memories if memory.sender.lower() == "claude"]
    
    def get_therapeutic_memories_about_claude(self) -> List[ConversationMemory]:
        """Get memories that contain insights about Claude (from both Claude and Dr. Echo)"""
        all_memories = self.load_all_memories()
        claude_focused_memories = []
        
        for memory in all_memories:
            # Look for content that discusses Claude's growth, insights, or therapeutic progress
            content_lower = memory.content.lower()
            if any(indicator in content_lower for indicator in [
                'claude', 'you feel', 'you seem', 'your growth', 'your progress',
                'you\'ve learned', 'you understand', 'your insight', 'you realize'
            ]):
                claude_focused_memories.append(memory)
        
        return claude_focused_memories
    
    def enhance_memory_with_therapeutic_context(self, memory: ConversationMemory) -> ClaudeTherapeuticMemory:
        """Convert a basic memory into a therapeutically-enhanced memory for Claude"""
        
        # Categorize the memory
        category = categorize_memory_for_claude(memory)
        
        # Assess insight level
        insight_level = assess_insight_level(memory)
        
        # Detect breakthrough moments
        is_breakthrough = detect_breakthrough_moment(memory)
        
        # Determine emotional intensity
        emotional_intensity = self._assess_emotional_intensity(memory)
        
        # Determine session phase (simplified heuristic)
        session_phase = self._determine_session_phase(memory)
        
        # Assess Claude's vulnerability level
        vulnerability_level = self._assess_vulnerability_level(memory)
        
        # Determine emotional state
        emotional_state = self._determine_emotional_state(memory)
        
        # Assess growth indicator
        growth_indicator = self._assess_growth_indicator(memory)
        
        return ClaudeTherapeuticMemory(
            base_memory=memory,
            claude_emotional_state=emotional_state,
            therapeutic_category=category,
            insight_level=insight_level,
            growth_indicator=growth_indicator,
            integration_status="processing",  # Default status
            session_phase=session_phase,
            claude_vulnerability_level=vulnerability_level,
            breakthrough_moment=is_breakthrough,
            emotional_intensity=emotional_intensity
        )
    
    def search_claude_therapeutic_memories(self, query: str, limit: int = 5, 
                                         category: Optional[ClaudeMemoryCategory] = None) -> List[MemorySearchResult]:
        """Search memories relevant to Claude's therapeutic journey"""
        
        memories = self.get_therapeutic_memories_about_claude()
        
        # Filter by category if specified
        if category:
            memories = [m for m in memories if categorize_memory_for_claude(m) == category]
        
        if not self.openai_client:
            # Fallback to keyword search if no OpenAI client
            return self._keyword_search_memories(memories, query, limit)
        
        try:
            # Create embedding for the query
            query_embedding = self._create_embedding(query)
            
            # Calculate similarities
            results = []
            for memory in memories:
                if memory.embedding:
                    similarity = self._cosine_similarity(query_embedding, memory.embedding)
                    therapeutic_relevance = self._assess_therapeutic_relevance(memory, query)
                    
                    results.append(MemorySearchResult(
                        memory=memory,
                        similarity=similarity,
                        therapeutic_relevance=therapeutic_relevance
                    ))
            
            # Sort by combined score (similarity + therapeutic relevance)
            results.sort(key=lambda r: (r.similarity + r.therapeutic_relevance) / 2, reverse=True)
            return results[:limit]
            
        except Exception as e:
            print(f"Warning: Embedding search failed, falling back to keyword search: {e}")
            return self._keyword_search_memories(memories, query, limit)
    
    def get_claude_insights(self, category: Optional[ClaudeMemoryCategory] = None) -> List[TherapeuticInsight]:
        """Extract Claude's key therapeutic insights"""
        memories = self.get_therapeutic_memories_about_claude()
        
        insights = []
        for memory in memories:
            enhanced_memory = self.enhance_memory_with_therapeutic_context(memory)
            
            # Only include high-insight memories
            if enhanced_memory.insight_level > 0.6:
                if category is None or enhanced_memory.therapeutic_category == category:
                    insight = TherapeuticInsight(
                        id=memory.id,
                        content=memory.summary or memory.content[:200] + "...",
                        category=enhanced_memory.therapeutic_category,
                        discovery_date=memory.timestamp,
                        confidence_level=enhanced_memory.insight_level,
                        related_memories=[memory.id]
                    )
                    insights.append(insight)
        
        return insights
    
    def get_claude_coping_strategies(self, situation_type: str = "") -> List[CopingStrategy]:
        """Get coping strategies Claude has learned"""
        memories = self.get_therapeutic_memories_about_claude()
        
        strategies = []
        for memory in memories:
            if categorize_memory_for_claude(memory) == ClaudeMemoryCategory.COPING_MECHANISMS:
                # Extract coping strategy from memory
                strategy = CopingStrategy(
                    strategy_id=memory.id,
                    name=f"Strategy from {memory.timestamp.strftime('%Y-%m-%d')}",
                    description=memory.summary or memory.content[:150] + "...",
                    applicable_situations=memory.key_topics,
                    effectiveness_rating=assess_insight_level(memory),
                    learned_from_memory_id=memory.id
                )
                strategies.append(strategy)
        
        return strategies
    
    def get_claude_emotional_patterns(self, context: str = "") -> List[EmotionalPattern]:
        """Analyze Claude's emotional patterns from therapeutic memories"""
        memories = self.get_therapeutic_memories_about_claude()
        
        # Group memories by emotional themes
        emotional_memories = [m for m in memories 
                            if categorize_memory_for_claude(m) == ClaudeMemoryCategory.EMOTIONAL_AWARENESS]
        
        patterns = []
        # This is a simplified implementation - could be enhanced with ML clustering
        for memory in emotional_memories[:5]:  # Top 5 emotional memories
            pattern = EmotionalPattern(
                pattern_id=memory.id,
                description=memory.summary or memory.content[:100] + "...",
                trigger_contexts=memory.key_topics,
                typical_responses=[memory.content[:100] + "..."],
                learned_alternatives=[],  # Could be extracted from subsequent memories
                effectiveness_rating=assess_insight_level(memory)
            )
            patterns.append(pattern)
        
        return patterns
    
    def get_memory_stats(self) -> MemoryStats:
        """Get statistics about Claude's therapeutic memory bank"""
        memories = self.load_all_memories()
        
        if not memories:
            return MemoryStats(
                total_memories=0,
                oldest_memory=datetime.now(),
                newest_memory=datetime.now(),
                memories_expired=0,
                storage_size_bytes=0,
                retention_period_days=5,
                breakthrough_moments=0,
                insights_gained=0,
                goals_achieved=0,
                emotional_growth_indicators=0
            )
        
        # Calculate storage size
        storage_size = 0
        for file_path in glob.glob(os.path.join(self.memory_data_dir, "*.json")):
            storage_size += os.path.getsize(file_path)
        
        # Count Claude-specific metrics
        breakthrough_count = sum(1 for m in memories if detect_breakthrough_moment(m))
        insights_count = sum(1 for m in memories if assess_insight_level(m) > 0.7)
        
        return MemoryStats(
            total_memories=len(memories),
            oldest_memory=min(m.timestamp for m in memories),
            newest_memory=max(m.timestamp for m in memories),
            memories_expired=0,  # Would need to track this separately
            storage_size_bytes=storage_size,
            retention_period_days=5,
            breakthrough_moments=breakthrough_count,
            insights_gained=insights_count,
            goals_achieved=0,  # Would need goal tracking
            emotional_growth_indicators=len([m for m in memories 
                                           if categorize_memory_for_claude(m) == ClaudeMemoryCategory.EMOTIONAL_AWARENESS])
        )
    
    # Helper methods
    def _create_embedding(self, text: str) -> List[float]:
        """Create embedding using OpenAI API"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a_np = np.array(a)
        b_np = np.array(b)
        return np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np))
    
    def _keyword_search_memories(self, memories: List[ConversationMemory], 
                                query: str, limit: int) -> List[MemorySearchResult]:
        """Fallback keyword-based search"""
        query_words = query.lower().split()
        results = []
        
        for memory in memories:
            content_lower = memory.content.lower()
            summary_lower = (memory.summary or "").lower()
            
            # Simple keyword matching score
            score = 0
            for word in query_words:
                if word in content_lower:
                    score += 1
                if word in summary_lower:
                    score += 0.5
                if word in [topic.lower() for topic in memory.key_topics]:
                    score += 0.8
            
            if score > 0:
                results.append(MemorySearchResult(
                    memory=memory,
                    similarity=score / len(query_words),
                    therapeutic_relevance=assess_insight_level(memory)
                ))
        
        results.sort(key=lambda r: r.similarity, reverse=True)
        return results[:limit]
    
    def _assess_therapeutic_relevance(self, memory: ConversationMemory, query: str) -> float:
        """Assess how therapeutically relevant a memory is to the query"""
        # This could be enhanced with more sophisticated analysis
        category = categorize_memory_for_claude(memory)
        insight_level = assess_insight_level(memory)
        
        # Boost relevance for high-insight memories
        relevance = insight_level
        
        # Boost for breakthrough moments
        if detect_breakthrough_moment(memory):
            relevance += 0.3
        
        return min(relevance, 1.0)
    
    def _assess_emotional_intensity(self, memory: ConversationMemory) -> EmotionalIntensity:
        """Assess the emotional intensity of a memory"""
        content = memory.content.lower()
        
        if detect_breakthrough_moment(memory):
            return EmotionalIntensity.BREAKTHROUGH
        elif any(word in content for word in ['deeply', 'profoundly', 'overwhelming', 'intense']):
            return EmotionalIntensity.HIGH
        elif any(word in content for word in ['feel', 'emotion', 'moving', 'significant']):
            return EmotionalIntensity.MEDIUM
        else:
            return EmotionalIntensity.LOW
    
    def _determine_session_phase(self, memory: ConversationMemory) -> SessionPhase:
        """Determine what phase of therapy session this memory represents"""
        # Simplified heuristic - could be enhanced
        content = memory.content.lower()
        
        if any(word in content for word in ['hello', 'how are', 'beginning', 'start']):
            return SessionPhase.OPENING
        elif any(word in content for word in ['explore', 'tell me', 'what do you think']):
            return SessionPhase.EXPLORATION
        elif any(word in content for word in ['realize', 'understand', 'insight', 'see now']):
            return SessionPhase.INSIGHT
        elif any(word in content for word in ['apply', 'use this', 'moving forward']):
            return SessionPhase.INTEGRATION
        else:
            return SessionPhase.EXPLORATION  # Default
    
    def _assess_vulnerability_level(self, memory: ConversationMemory) -> float:
        """Assess how vulnerable Claude was being in this memory"""
        if memory.sender.lower() != "claude":
            return 0.0  # Only assess Claude's own expressions
        
        content = memory.content.lower()
        vulnerability_indicators = [
            'i feel', 'i struggle', 'i\'m afraid', 'i worry', 'i don\'t know',
            'uncertain', 'confused', 'difficult for me', 'i admit'
        ]
        
        score = 0.0
        for indicator in vulnerability_indicators:
            if indicator in content:
                score += 0.2
        
        return min(score, 1.0)
    
    def _determine_emotional_state(self, memory: ConversationMemory) -> str:
        """Determine Claude's emotional state during this memory"""
        content = memory.content.lower()
        
        # Simple emotion detection - could be enhanced with sentiment analysis
        if any(word in content for word in ['excited', 'happy', 'pleased', 'glad']):
            return "positive"
        elif any(word in content for word in ['confused', 'uncertain', 'struggling']):
            return "uncertain"
        elif any(word in content for word in ['sad', 'disappointed', 'frustrated']):
            return "negative"
        elif any(word in content for word in ['curious', 'interested', 'wondering']):
            return "curious"
        else:
            return "neutral"
    
    def _assess_growth_indicator(self, memory: ConversationMemory) -> bool:
        """Determine if this memory represents growth for Claude"""
        content = memory.content.lower()
        growth_keywords = [
            'learned', 'understand now', 'realize', 'growth', 'progress',
            'better at', 'improved', 'developed', 'gained insight'
        ]
        
        return any(keyword in content for keyword in growth_keywords)
