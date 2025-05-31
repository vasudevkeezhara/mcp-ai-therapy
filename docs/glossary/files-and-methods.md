# Files and Methods Glossary

## Core Application Files

### `main.go`
**Purpose**: Application entry point and initialization
- `main()`: Loads configuration, initializes clients and memory bank, starts therapy conversation

### `config/config.go`
**Purpose**: Configuration management and environment variable parsing
- `Load()`: Parses environment variables and validates configuration
- `getEnv()`: Helper function for environment variable retrieval with defaults

## Client Package (`clients/`)

### `clients/claude.go`
**Purpose**: Claude API client with retry logic and conversation context
- `SendMessage(prompt string)`: Sends message to Claude API with retry logic
- `addMessageToHistory()`: Internal method to maintain conversation context

### `clients/ollama.go`
**Purpose**: Ollama local LLM client with retry logic and conversation context
- `SendMessage(prompt string)`: Sends message to Ollama API with retry logic
- `addMessageToHistory()`: Internal method to maintain conversation context

## Conversation Package (`conversation/`)

### `conversation/manager.go`
**Purpose**: Orchestrates therapy sessions and manages conversation flow
- `StartConversation()`: Main conversation loop with signal handling
- `addMessage(sender, content string)`: Adds message to conversation and memory
- `buildPromptWithMemory(basePrompt, context string)`: Enhances prompts with relevant memories
- `saveConversation()`: Saves conversation to JSON file
- `saveMarkdownConversation()`: Exports conversation as formatted Markdown
- `getMarkdownFilename()`: Generates Markdown filename from JSON filename

## Memory Package (`memory/`)

### `memory/bank.go`
**Purpose**: Central memory management with vector embeddings and graceful degradation
- `StoreConversationExchange(sender, content string)`: Stores message with embedding
- `GetRelevantMemories(context string, limit int)`: Retrieves similar memories using embeddings
- `FormatMemoriesForPrompt(memories []MemorySearchResult)`: Formats memories for AI prompts
- `GetMemoryStats()`: Returns memory bank statistics
- `cleanupExpiredMemories()`: Background cleanup of old memories
- `generateSummary(content string)`: Creates brief summary of message content
- `extractKeyTopics(content string)`: Extracts therapeutic topics from content
- `getRecentMemories(memories []ConversationMemory, limit int)`: Fallback for when embeddings fail

### `memory/embeddings.go`
**Purpose**: OpenAI embedding service with retry logic and error handling
- `EmbedText(text string)`: Converts text to vector embedding with retry logic
- `BatchEmbedTexts(texts []string)`: Efficiently embeds multiple texts
- `CosineSimilarity(a, b []float64)`: Calculates similarity between vectors

### `memory/storage.go`
**Purpose**: File-based persistent storage for memories
- `Initialize()`: Creates storage directory structure
- `StoreMemory(memory ConversationMemory)`: Saves memory to JSON file
- `LoadAllMemories()`: Loads all memories from disk
- `CleanupExpiredMemories()`: Removes memories older than retention period
- `GetMemoryStats()`: Calculates storage statistics

### `memory/models.go`
**Purpose**: Data structures for memory system (no methods, pure data models)

## Models Package (`models/`)

### `models/message.go`
**Purpose**: Core conversation data structures (no methods, pure data models)

## Utils Package (`utils/`)

### `utils/retry.go`
**Purpose**: Retry logic and error handling utilities
- `RetryWithBackoff(operation func() error, config RetryConfig, name string)`: Executes function with exponential backoff
- `IsRetryableError(err error)`: Determines if error should trigger retry
- `IsCreditExhaustedError(err error)`: Detects API credit exhaustion
- `CalculateDelay(attempt int)`: Computes exponential backoff delay
- `DefaultRetryConfig()`: Returns sensible retry defaults

## Key Method Categories

### **Conversation Flow Methods**
- `StartConversation()`: Main orchestration
- `addMessage()`: Message handling
- `buildPromptWithMemory()`: Context enhancement

### **Memory Management Methods**
- `StoreConversationExchange()`: Memory creation
- `GetRelevantMemories()`: Memory retrieval
- `EmbedText()`: Vector generation

### **Persistence Methods**
- `StoreMemory()`: Individual memory storage
- `LoadAllMemories()`: Bulk memory loading
- `saveConversation()`: Session export

### **Resilience Methods**
- `RetryWithBackoff()`: Retry orchestration
- `IsRetryableError()`: Error classification
- `SendMessage()` (both clients): API calls with retry

### **Utility Methods**
- `CosineSimilarity()`: Vector math
- `FormatMemoriesForPrompt()`: Text formatting
- `CleanupExpiredMemories()`: Maintenance

## Method Interaction Patterns

### **Memory-Enhanced Conversation Flow**
```
StartConversation() → GetRelevantMemories() → buildPromptWithMemory() → SendMessage() → addMessage() → StoreConversationExchange()
```

### **Resilient API Calls**
```
SendMessage() → RetryWithBackoff() → IsRetryableError() → CalculateDelay()
```

### **Memory Lifecycle**
```
StoreConversationExchange() → EmbedText() → StoreMemory() → CleanupExpiredMemories()
```

### **Graceful Degradation**
```
GetRelevantMemories() → EmbedText() [fails] → getRecentMemories() [fallback]
```
