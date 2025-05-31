package memory

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"time"

	"github.com/google/uuid"
)

// MemoryStorage handles persistent storage of memories
type MemoryStorage struct {
	dataDir         string
	retentionPeriod time.Duration
}

// NewMemoryStorage creates a new memory storage instance
func NewMemoryStorage(dataDir string, retentionPeriod time.Duration) *MemoryStorage {
	return &MemoryStorage{
		dataDir:         dataDir,
		retentionPeriod: retentionPeriod,
	}
}

// Initialize creates the data directory if it doesn't exist
func (ms *MemoryStorage) Initialize() error {
	return os.MkdirAll(ms.dataDir, 0755)
}

// StoreMemory saves a memory to disk
func (ms *MemoryStorage) StoreMemory(memory ConversationMemory) error {
	if memory.ID == "" {
		memory.ID = uuid.New().String()
	}

	filename := fmt.Sprintf("%s.json", memory.ID)
	filepath := filepath.Join(ms.dataDir, filename)

	data, err := json.MarshalIndent(memory, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal memory: %v", err)
	}

	return os.WriteFile(filepath, data, 0644)
}

// LoadAllMemories loads all memories from disk
func (ms *MemoryStorage) LoadAllMemories() ([]ConversationMemory, error) {
	files, err := filepath.Glob(filepath.Join(ms.dataDir, "*.json"))
	if err != nil {
		return nil, fmt.Errorf("failed to list memory files: %v", err)
	}

	var memories []ConversationMemory
	for _, file := range files {
		data, err := os.ReadFile(file)
		if err != nil {
			continue // Skip corrupted files
		}

		var memory ConversationMemory
		if err := json.Unmarshal(data, &memory); err != nil {
			continue // Skip corrupted files
		}

		memories = append(memories, memory)
	}

	return memories, nil
}

// CleanupExpiredMemories removes memories older than retention period
func (ms *MemoryStorage) CleanupExpiredMemories() (int, error) {
	memories, err := ms.LoadAllMemories()
	if err != nil {
		return 0, err
	}

	cutoff := time.Now().Add(-ms.retentionPeriod)
	expired := 0

	for _, memory := range memories {
		if memory.Timestamp.Before(cutoff) {
			filename := fmt.Sprintf("%s.json", memory.ID)
			filepath := filepath.Join(ms.dataDir, filename)
			if err := os.Remove(filepath); err == nil {
				expired++
			}
		}
	}

	return expired, nil
}

// GetMemoryStats returns statistics about stored memories
func (ms *MemoryStorage) GetMemoryStats() (MemoryStats, error) {
	memories, err := ms.LoadAllMemories()
	if err != nil {
		return MemoryStats{}, err
	}

	if len(memories) == 0 {
		return MemoryStats{
			TotalMemories:   0,
			RetentionPeriod: ms.retentionPeriod,
		}, nil
	}

	// Sort by timestamp to find oldest/newest
	sort.Slice(memories, func(i, j int) bool {
		return memories[i].Timestamp.Before(memories[j].Timestamp)
	})

	// Calculate storage size
	var storageSize int64
	files, _ := filepath.Glob(filepath.Join(ms.dataDir, "*.json"))
	for _, file := range files {
		if info, err := os.Stat(file); err == nil {
			storageSize += info.Size()
		}
	}

	return MemoryStats{
		TotalMemories:   len(memories),
		OldestMemory:    memories[0].Timestamp,
		NewestMemory:    memories[len(memories)-1].Timestamp,
		StorageSize:     storageSize,
		RetentionPeriod: ms.retentionPeriod,
	}, nil
}
