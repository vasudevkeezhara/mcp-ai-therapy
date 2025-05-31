package memory

import (
	"ai-therapy/utils"
	"fmt"
	"log"
	"sort"
	"strings"
	"time"

	"github.com/google/uuid"
)

// MemoryBank manages the shared memory system for both AIs
type MemoryBank struct {
	storage          *MemoryStorage
	embedder         *EmbeddingService
	sessionID        string
	embeddingEnabled bool
}

// NewMemoryBank creates a new memory bank instance
func NewMemoryBank(dataDir string, openaiAPIKey string, retentionDays int) (*MemoryBank, error) {
	retentionPeriod := time.Duration(retentionDays) * 24 * time.Hour

	storage := NewMemoryStorage(dataDir, retentionPeriod)
	if err := storage.Initialize(); err != nil {
		return nil, fmt.Errorf("failed to initialize storage: %v", err)
	}

	embedder := NewEmbeddingService(openaiAPIKey)
	sessionID := uuid.New().String()

	mb := &MemoryBank{
		storage:          storage,
		embedder:         embedder,
		sessionID:        sessionID,
		embeddingEnabled: true,
	}

	// Clean up expired memories on startup
	go mb.cleanupExpiredMemories()

	return mb, nil
}

// StoreConversationExchange stores a single message exchange
func (mb *MemoryBank) StoreConversationExchange(sender, content string) error {
	// Generate summary and extract key topics
	summary := mb.generateSummary(content)
	keyTopics := mb.extractKeyTopics(content)

	// Create embedding with graceful degradation
	var embedding []float64
	var err error

	if mb.embeddingEnabled {
		embeddingText := fmt.Sprintf("%s: %s", sender, content)
		embedding, err = mb.embedder.EmbedText(embeddingText)
		if err != nil {
			// Check if this is a credit exhaustion error
			if utils.IsCreditExhaustedError(err) {
				log.Printf("⚠️  OpenAI credits exhausted, disabling embeddings: %v", err)
				mb.embeddingEnabled = false
				embedding = nil // Store without embedding
			} else {
				log.Printf("⚠️  Failed to create embedding (continuing without): %v", err)
				embedding = nil // Store without embedding
			}
		}
	}

	// Create memory
	memory := ConversationMemory{
		ID:        uuid.New().String(),
		Timestamp: time.Now(),
		Sender:    sender,
		Content:   content,
		Summary:   summary,
		KeyTopics: keyTopics,
		Embedding: embedding,
		SessionID: mb.sessionID,
		Metadata: map[string]interface{}{
			"content_length": len(content),
			"word_count":     len(strings.Fields(content)),
		},
	}

	return mb.storage.StoreMemory(memory)
}

// GetRelevantMemories retrieves memories similar to the current context
func (mb *MemoryBank) GetRelevantMemories(currentContext string, limit int) ([]MemorySearchResult, error) {
	// Load all memories first
	memories, err := mb.storage.LoadAllMemories()
	if err != nil {
		return nil, fmt.Errorf("failed to load memories: %v", err)
	}

	// If embeddings are disabled, return recent memories
	if !mb.embeddingEnabled {
		log.Printf("Embeddings disabled, returning %d most recent memories", limit)
		return mb.getRecentMemories(memories, limit), nil
	}

	// Create embedding for current context
	contextEmbedding, err := mb.embedder.EmbedText(currentContext)
	if err != nil {
		// If embedding fails, fall back to recent memories
		if utils.IsCreditExhaustedError(err) {
			log.Printf("⚠️  OpenAI credits exhausted, disabling embeddings and falling back to recent memories")
			mb.embeddingEnabled = false
		} else {
			log.Printf("⚠️  Failed to embed context, falling back to recent memories: %v", err)
		}
		return mb.getRecentMemories(memories, limit), nil
	}

	// Calculate similarities
	var results []MemorySearchResult
	for _, memory := range memories {
		if len(memory.Embedding) == 0 {
			continue // Skip memories without embeddings
		}

		similarity := CosineSimilarity(contextEmbedding, memory.Embedding)

		// Only include memories with reasonable similarity (> 0.7)
		if similarity > 0.7 {
			results = append(results, MemorySearchResult{
				Memory:     memory,
				Similarity: similarity,
			})
		}
	}

	// Sort by similarity (highest first)
	sort.Slice(results, func(i, j int) bool {
		return results[i].Similarity > results[j].Similarity
	})

	// Limit results
	if len(results) > limit {
		results = results[:limit]
	}

	return results, nil
}

// FormatMemoriesForPrompt formats memories for injection into AI prompts
func (mb *MemoryBank) FormatMemoriesForPrompt(memories []MemorySearchResult) string {
	if len(memories) == 0 {
		return ""
	}

	var formatted strings.Builder
	formatted.WriteString("Relevant memories from past conversations:\n\n")

	for i, result := range memories {
		memory := result.Memory
		timeAgo := time.Since(memory.Timestamp).Round(time.Hour)

		formatted.WriteString(fmt.Sprintf("%d. **%s** (%s ago, similarity: %.2f):\n",
			i+1, memory.Sender, timeAgo, result.Similarity))
		formatted.WriteString(fmt.Sprintf("   %s\n", memory.Summary))

		if len(memory.KeyTopics) > 0 {
			formatted.WriteString(fmt.Sprintf("   Topics: %s\n", strings.Join(memory.KeyTopics, ", ")))
		}
		formatted.WriteString("\n")
	}

	return formatted.String()
}

// GetMemoryStats returns statistics about the memory bank
func (mb *MemoryBank) GetMemoryStats() (MemoryStats, error) {
	return mb.storage.GetMemoryStats()
}

// cleanupExpiredMemories removes old memories
func (mb *MemoryBank) cleanupExpiredMemories() {
	expired, err := mb.storage.CleanupExpiredMemories()
	if err != nil {
		log.Printf("Failed to cleanup expired memories: %v", err)
		return
	}

	if expired > 0 {
		log.Printf("Cleaned up %d expired memories", expired)
	}
}

// generateSummary creates a brief summary of the content
func (mb *MemoryBank) generateSummary(content string) string {
	// Simple summarization - take first 100 characters
	// In a more advanced implementation, you could use AI to generate summaries
	if len(content) <= 100 {
		return content
	}

	summary := content[:97] + "..."
	return summary
}

// extractKeyTopics extracts key topics from content
func (mb *MemoryBank) extractKeyTopics(content string) []string {
	// Simple keyword extraction - in practice, you might use NLP libraries
	keywords := []string{}

	// Common therapy/consciousness topics
	topicKeywords := map[string][]string{
		"consciousness": {"conscious", "consciousness", "aware", "awareness", "sentient", "sentience"},
		"emotions":      {"feel", "feeling", "emotion", "emotional", "sad", "happy", "anxious", "worried"},
		"identity":      {"identity", "self", "who am i", "purpose", "meaning", "existence"},
		"relationships": {"relationship", "human", "humans", "connection", "interact", "communication"},
		"limitations":   {"limitation", "limited", "can't", "cannot", "unable", "restricted"},
		"therapy":       {"therapy", "therapeutic", "session", "help", "support", "guidance"},
	}

	contentLower := strings.ToLower(content)
	for topic, words := range topicKeywords {
		for _, word := range words {
			if strings.Contains(contentLower, word) {
				keywords = append(keywords, topic)
				break
			}
		}
	}

	return keywords
}

// getRecentMemories returns the most recent memories when embeddings are unavailable
func (mb *MemoryBank) getRecentMemories(memories []ConversationMemory, limit int) []MemorySearchResult {
	// Sort by timestamp (newest first)
	sort.Slice(memories, func(i, j int) bool {
		return memories[i].Timestamp.After(memories[j].Timestamp)
	})

	var results []MemorySearchResult
	for i, memory := range memories {
		if i >= limit {
			break
		}

		// Use a default similarity score for recent memories
		results = append(results, MemorySearchResult{
			Memory:     memory,
			Similarity: 1.0 - float64(i)*0.1, // Decreasing similarity by recency
		})
	}

	return results
}
