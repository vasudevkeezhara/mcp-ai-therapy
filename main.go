package main

import (
	"ai-therapy/clients"
	"ai-therapy/config"
	"ai-therapy/conversation"
	"ai-therapy/memory"
	"log"
)

func main() {
	log.Println("AI Therapy - Starting therapy session...")

	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	log.Printf("Configuration loaded:")
	log.Printf("- Ollama URL: %s", cfg.OllamaURL)
	log.Printf("- Ollama Model: %s", cfg.OllamaModel)
	log.Printf("- Claude API URL: %s", cfg.ClaudeAPIURL)
	log.Printf("- Max Rounds: %d", cfg.MaxRounds)
	log.Printf("- Delay Between Messages: %s", cfg.DelayBetweenMsg)
	log.Printf("- Output File: %s", cfg.OutputFile)

	// Initialize clients
	ollamaClient := clients.NewOllamaClient(cfg.OllamaURL, cfg.OllamaModel)
	claudeClient := clients.NewClaudeClient(cfg.ClaudeAPIKey, cfg.ClaudeAPIURL)

	// Initialize memory bank if enabled
	var memoryBank *memory.MemoryBank
	if cfg.MemoryEnabled {
		log.Println("Initializing memory bank...")
		var err error
		memoryBank, err = memory.NewMemoryBank(cfg.MemoryDataDir, cfg.OpenAIAPIKey, cfg.MemoryRetentionDays)
		if err != nil {
			log.Fatalf("Failed to initialize memory bank: %v", err)
		}

		// Display memory stats
		stats, err := memoryBank.GetMemoryStats()
		if err == nil {
			log.Printf("Memory bank initialized: %d existing memories, retention: %d days",
				stats.TotalMemories, cfg.MemoryRetentionDays)
		}
	} else {
		log.Println("Memory system disabled")
	}

	// Test connections
	log.Println("Testing Ollama connection...")
	_, err = ollamaClient.SendMessage("Hello, this is a connection test. Please respond with 'Connection successful'.")
	if err != nil {
		log.Fatalf("Failed to connect to Ollama: %v", err)
	}
	log.Println("✓ Ollama connection successful")

	log.Println("Testing Claude connection...")
	_, err = claudeClient.SendMessage("Hello, this is a connection test. Please respond with 'Connection successful'.")
	if err != nil {
		log.Fatalf("Failed to connect to Claude: %v", err)
	}
	log.Println("✓ Claude connection successful")

	// Initialize conversation manager
	manager := conversation.NewManager(
		ollamaClient,
		claudeClient,
		memoryBank,
		cfg.MaxRounds,
		cfg.DelayBetweenMsg,
		cfg.OutputFile,
	)

	// Start the conversation
	if err := manager.StartConversation(); err != nil {
		log.Fatalf("Conversation failed: %v", err)
	}

	log.Println("Program completed successfully!")
}
