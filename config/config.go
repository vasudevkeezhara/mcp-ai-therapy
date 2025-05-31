package config

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
)

type Config struct {
	// Claude API configuration
	ClaudeAPIKey string
	ClaudeAPIURL string

	// Ollama configuration
	OllamaURL   string
	OllamaModel string

	// Memory configuration
	MemoryEnabled       bool
	MemoryDataDir       string
	MemoryRetentionDays int
	OpenAIAPIKey        string

	// Conversation settings
	MaxRounds       int
	DelayBetweenMsg time.Duration
	OutputFile      string
}

func Load() (*Config, error) {
	// Load .env file if it exists
	_ = godotenv.Load()

	// Generate timestamped filename if OUTPUT_FILE is not explicitly set
	defaultOutputFile := generateTimestampedFilename()

	config := &Config{
		ClaudeAPIKey:        getEnv("CLAUDE_API_KEY", ""),
		ClaudeAPIURL:        getEnv("CLAUDE_API_URL", "https://api.anthropic.com/v1/messages"),
		OllamaURL:           getEnv("OLLAMA_URL", "http://localhost:11434"),
		OllamaModel:         getEnv("OLLAMA_MODEL", "llama2"),
		MemoryEnabled:       getEnv("MEMORY_ENABLED", "true") == "true",
		MemoryDataDir:       getEnv("MEMORY_DATA_DIR", "./memory_data"),
		MemoryRetentionDays: 5, // Will be parsed below
		OpenAIAPIKey:        getEnv("OPENAI_API_KEY", ""),
		OutputFile:          getEnv("OUTPUT_FILE", defaultOutputFile),
	}

	// Parse max rounds
	maxRoundsStr := getEnv("MAX_ROUNDS", "100")
	maxRounds, err := strconv.Atoi(maxRoundsStr)
	if err != nil {
		return nil, fmt.Errorf("invalid MAX_ROUNDS value: %v", err)
	}
	config.MaxRounds = maxRounds

	// Parse memory retention days
	retentionStr := getEnv("MEMORY_RETENTION_DAYS", "5")
	retentionDays, err := strconv.Atoi(retentionStr)
	if err != nil {
		return nil, fmt.Errorf("invalid MEMORY_RETENTION_DAYS value: %v", err)
	}
	config.MemoryRetentionDays = retentionDays

	// Parse delay between messages
	delayStr := getEnv("DELAY_BETWEEN_MSG", "3s")
	delay, err := time.ParseDuration(delayStr)
	if err != nil {
		return nil, fmt.Errorf("invalid DELAY_BETWEEN_MSG value: %v", err)
	}
	config.DelayBetweenMsg = delay

	// Validate required fields
	if config.ClaudeAPIKey == "" {
		return nil, fmt.Errorf("CLAUDE_API_KEY is required")
	}

	// Validate memory configuration if enabled
	if config.MemoryEnabled && config.OpenAIAPIKey == "" {
		return nil, fmt.Errorf("OPENAI_API_KEY is required when memory is enabled")
	}

	return config, nil
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// generateTimestampedFilename creates a timestamped filename for therapy sessions
// Format: conversations/therapy_session_YYYY-MM-DD_HH.json
func generateTimestampedFilename() string {
	now := time.Now()
	timestamp := now.Format("2006-01-02_15")
	return fmt.Sprintf("conversations/therapy_session_%s.json", timestamp)
}
