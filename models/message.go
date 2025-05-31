package models

import "time"

// Message represents a single message in the conversation
type Message struct {
	ID        int       `json:"id"`
	Sender    string    `json:"sender"`    // "ollama" or "claude"
	Content   string    `json:"content"`
	Timestamp time.Time `json:"timestamp"`
}

// Conversation represents the entire conversation history
type Conversation struct {
	Messages    []Message `json:"messages"`
	StartTime   time.Time `json:"start_time"`
	EndTime     time.Time `json:"end_time"`
	TotalRounds int       `json:"total_rounds"`
}
