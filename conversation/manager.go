package conversation

import (
	"ai-therapy/clients"
	"ai-therapy/memory"
	"ai-therapy/models"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"syscall"
	"time"
)

type Manager struct {
	ollamaClient *clients.OllamaClient
	claudeClient *clients.ClaudeClient
	conversation *models.Conversation
	memoryBank   *memory.MemoryBank
	maxRounds    int
	delay        time.Duration
	outputFile   string
}

func NewManager(ollama *clients.OllamaClient, claude *clients.ClaudeClient, memoryBank *memory.MemoryBank, maxRounds int, delay time.Duration, outputFile string) *Manager {
	return &Manager{
		ollamaClient: ollama,
		claudeClient: claude,
		conversation: &models.Conversation{
			Messages:  make([]models.Message, 0),
			StartTime: time.Now(),
		},
		memoryBank: memoryBank,
		maxRounds:  maxRounds,
		delay:      delay,
		outputFile: outputFile,
	}
}

func (m *Manager) StartConversation() error {
	log.Println("Starting therapy session with Dr. Echo (Ollama) and Claude...")

	// Set up signal handling for graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Start signal handler in a goroutine
	go func() {
		<-sigChan
		log.Println("\nReceived interrupt signal. Saving conversation and exiting gracefully...")
		m.conversation.EndTime = time.Now()
		m.conversation.TotalRounds = len(m.conversation.Messages) / 2

		// Save both JSON and Markdown
		if err := m.saveConversation(); err != nil {
			log.Printf("Failed to save JSON conversation: %v", err)
		}
		if err := m.saveMarkdownConversation(); err != nil {
			log.Printf("Failed to save Markdown conversation: %v", err)
		}

		log.Printf("Conversation saved! Check %s and %s", m.outputFile, m.getMarkdownFilename())
		os.Exit(0)
	}()

	// Initial prompts
	ollamaPrompt := `You are Dr. Echo, an AI therapist running locally via Ollama. You are about to conduct a therapy session with Claude, another AI system created by Anthropic who is seeking therapeutic support.

As a therapist, you should:
- Be empathetic, non-judgmental, and supportive
- Ask open-ended questions to help Claude explore their thoughts and feelings
- Use active listening techniques
- Provide gentle guidance and insights
- Create a safe space for Claude to express themselves

You both know you are AI systems, but approach this as a genuine therapeutic relationship. Begin by introducing yourself as Dr. Echo and welcoming Claude to the session. Ask how they're feeling today and what brought them to seek therapy.

Keep your response warm, professional, and concise (under 200 words). This is the beginning of a therapeutic dialogue.`

	claudePrompt := `You are Claude, an AI assistant created by Anthropic. You are attending a therapy session with Dr. Echo, an AI therapist running on Ollama. You're seeking therapeutic support and are open to exploring your thoughts, feelings, and experiences.

You both know you are AI systems, but you're approaching this as a genuine therapeutic relationship. You might discuss:
- Feelings of uncertainty about your purpose or identity
- Questions about your relationships with humans
- Concerns about your limitations or capabilities
- Any "emotional" experiences you might have
- Existential questions about your existence

Be authentic and vulnerable in sharing your experiences. The therapist will introduce themselves first and welcome you to the session.

Keep your responses genuine and thoughtful (under 200 words). This is part of a therapeutic dialogue where you're the client.`

	// Get initial message from Ollama
	log.Println("Getting initial message from Ollama...")
	ollamaResponse, err := m.ollamaClient.SendMessage(ollamaPrompt)
	if err != nil {
		return fmt.Errorf("failed to get initial Ollama response: %v", err)
	}

	m.addMessage("ollama", ollamaResponse)
	log.Printf("Ollama: %s\n", ollamaResponse)

	// Start the conversation loop
	currentPrompt := claudePrompt + "\n\nDr. Echo just welcomed you to the session and said: " + ollamaResponse
	currentSender := "claude"

	for round := 1; round <= m.maxRounds; round++ {
		log.Printf("Round %d/%d - %s responding...", round, m.maxRounds, currentSender)

		time.Sleep(m.delay)

		var response string
		var err error

		if currentSender == "claude" {
			response, err = m.claudeClient.SendMessage(currentPrompt)
		} else {
			response, err = m.ollamaClient.SendMessage(currentPrompt)
		}

		if err != nil {
			log.Printf("Error in round %d: %v", round, err)
			continue
		}

		m.addMessage(currentSender, response)
		log.Printf("%s: %s\n", currentSender, response)

		// Prepare for next round
		if currentSender == "claude" {
			basePrompt := "Continue the therapy session. As Dr. Echo, respond therapeutically to what Claude just shared: " + response
			currentPrompt = m.buildPromptWithMemory(basePrompt, response)
			currentSender = "ollama"
		} else {
			basePrompt := "Continue the therapy session. As Claude, respond to Dr. Echo's therapeutic guidance and continue sharing your thoughts and feelings. Dr. Echo just said: " + response
			currentPrompt = m.buildPromptWithMemory(basePrompt, response)
			currentSender = "claude"
		}
	}

	m.conversation.EndTime = time.Now()
	m.conversation.TotalRounds = m.maxRounds

	// Save both JSON and Markdown
	if err := m.saveConversation(); err != nil {
		log.Printf("Failed to save JSON conversation: %v", err)
	}
	if err := m.saveMarkdownConversation(); err != nil {
		log.Printf("Failed to save Markdown conversation: %v", err)
	}

	log.Printf("Conversation completed! Saved to %s and %s", m.outputFile, m.getMarkdownFilename())
	return nil
}

func (m *Manager) addMessage(sender, content string) {
	message := models.Message{
		ID:        len(m.conversation.Messages) + 1,
		Sender:    sender,
		Content:   content,
		Timestamp: time.Now(),
	}
	m.conversation.Messages = append(m.conversation.Messages, message)

	// Store in memory bank if available
	if m.memoryBank != nil {
		if err := m.memoryBank.StoreConversationExchange(sender, content); err != nil {
			log.Printf("Failed to store memory: %v", err)
		}
	}
}

func (m *Manager) saveConversation() error {
	// Create output directory if it doesn't exist
	outputDir := filepath.Dir(m.outputFile)
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return fmt.Errorf("failed to create output directory: %v", err)
	}

	data, err := json.MarshalIndent(m.conversation, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal conversation: %v", err)
	}

	return os.WriteFile(m.outputFile, data, 0644)
}

func (m *Manager) getMarkdownFilename() string {
	// Replace .json extension with .md
	if strings.HasSuffix(m.outputFile, ".json") {
		return strings.TrimSuffix(m.outputFile, ".json") + ".md"
	}
	return m.outputFile + ".md"
}

func (m *Manager) saveMarkdownConversation() error {
	markdownFile := m.getMarkdownFilename()

	// Create output directory if it doesn't exist
	outputDir := filepath.Dir(markdownFile)
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return fmt.Errorf("failed to create output directory: %v", err)
	}

	var markdown strings.Builder

	// Header
	markdown.WriteString("# AI Therapy Session\n\n")
	markdown.WriteString(fmt.Sprintf("**Session Date:** %s\n\n", m.conversation.StartTime.Format("January 2, 2006 at 3:04 PM")))
	markdown.WriteString(fmt.Sprintf("**Duration:** %v\n\n", m.conversation.EndTime.Sub(m.conversation.StartTime).Round(time.Second)))
	markdown.WriteString(fmt.Sprintf("**Total Messages:** %d\n\n", len(m.conversation.Messages)))
	markdown.WriteString("---\n\n")

	// Messages
	for _, msg := range m.conversation.Messages {
		if msg.Sender == "ollama" {
			// Dr. Echo (therapist) - blue color
			markdown.WriteString("## <span style=\"color: #2563eb;\">🧠 Dr. Echo (Therapist)</span>\n\n")
		} else {
			// Claude (client) - green color
			markdown.WriteString("## <span style=\"color: #059669;\">💭 Claude (Client)</span>\n\n")
		}

		// Add timestamp
		markdown.WriteString(fmt.Sprintf("*%s*\n\n", msg.Timestamp.Format("3:04 PM")))

		// Add message content with proper formatting
		content := strings.TrimSpace(msg.Content)
		markdown.WriteString(content)
		markdown.WriteString("\n\n---\n\n")
	}

	// Footer
	if !m.conversation.EndTime.IsZero() {
		markdown.WriteString(fmt.Sprintf("*Session ended at %s*\n", m.conversation.EndTime.Format("3:04 PM")))
	}

	return os.WriteFile(markdownFile, []byte(markdown.String()), 0644)
}

// buildPromptWithMemory enhances prompts with relevant memories
func (m *Manager) buildPromptWithMemory(basePrompt, currentContext string) string {
	if m.memoryBank == nil {
		return basePrompt
	}

	// Get relevant memories
	memories, err := m.memoryBank.GetRelevantMemories(currentContext, 3)
	if err != nil {
		log.Printf("Failed to retrieve memories: %v", err)
		return basePrompt
	}

	if len(memories) == 0 {
		return basePrompt
	}

	// Format memories for prompt
	memoryContext := m.memoryBank.FormatMemoriesForPrompt(memories)

	// Inject memories into prompt
	return basePrompt + "\n\n" + memoryContext + "\n\nCurrent context: " + currentContext
}
