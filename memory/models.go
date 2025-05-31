package memory

import (
	"time"
)

// ConversationMemory represents a single exchange in the conversation
type ConversationMemory struct {
	ID           string                 `json:"id"`
	Timestamp    time.Time              `json:"timestamp"`
	Sender       string                 `json:"sender"`       // "ollama" or "claude"
	Content      string                 `json:"content"`      // The actual message
	Summary      string                 `json:"summary"`      // AI-generated summary
	KeyTopics    []string               `json:"key_topics"`   // Extracted topics
	Embedding    []float64              `json:"embedding"`    // Vector embedding
	SessionID    string                 `json:"session_id"`   // Links to conversation session
	Metadata     map[string]interface{} `json:"metadata"`     // Additional context
}

// MemorySearchResult represents a memory with similarity score
type MemorySearchResult struct {
	Memory     ConversationMemory `json:"memory"`
	Similarity float64            `json:"similarity"`
}

// MemoryStats provides statistics about the memory bank
type MemoryStats struct {
	TotalMemories   int           `json:"total_memories"`
	OldestMemory    time.Time     `json:"oldest_memory"`
	NewestMemory    time.Time     `json:"newest_memory"`
	MemoriesExpired int           `json:"memories_expired"`
	StorageSize     int64         `json:"storage_size_bytes"`
	RetentionPeriod time.Duration `json:"retention_period"`
}
