# Data Models

## Core Data Structures

### Message Models

#### `models.Message`
```go
type Message struct {
    ID        int       `json:"id"`
    Sender    string    `json:"sender"`    // "ollama" or "claude"
    Content   string    `json:"content"`
    Timestamp time.Time `json:"timestamp"`
}
```
**Purpose**: Represents a single message in the current conversation session.

#### `models.Conversation`
```go
type Conversation struct {
    Messages    []Message `json:"messages"`
    StartTime   time.Time `json:"start_time"`
    EndTime     time.Time `json:"end_time"`
    TotalRounds int       `json:"total_rounds"`
}
```
**Purpose**: Contains the complete conversation session with metadata.

### Memory Models

#### `memory.ConversationMemory`
```go
type ConversationMemory struct {
    ID           string                 `json:"id"`
    Timestamp    time.Time              `json:"timestamp"`
    Sender       string                 `json:"sender"`
    Content      string                 `json:"content"`
    Summary      string                 `json:"summary"`
    KeyTopics    []string               `json:"key_topics"`
    Embedding    []float64              `json:"embedding"`
    SessionID    string                 `json:"session_id"`
    Metadata     map[string]interface{} `json:"metadata"`
}
```
**Purpose**: Persistent memory storage with semantic embeddings for cross-session context.

#### `memory.MemorySearchResult`
```go
type MemorySearchResult struct {
    Memory     ConversationMemory `json:"memory"`
    Similarity float64            `json:"similarity"`
}
```
**Purpose**: Represents a memory with its similarity score for ranking search results.

#### `memory.MemoryStats`
```go
type MemoryStats struct {
    TotalMemories   int           `json:"total_memories"`
    OldestMemory    time.Time     `json:"oldest_memory"`
    NewestMemory    time.Time     `json:"newest_memory"`
    MemoriesExpired int           `json:"memories_expired"`
    StorageSize     int64         `json:"storage_size_bytes"`
    RetentionPeriod time.Duration `json:"retention_period"`
}
```
**Purpose**: Provides insights into memory bank health and usage.

### API Client Models

#### Claude API Models
```go
type ClaudeMessage struct {
    Role    string `json:"role"`    // "user" or "assistant"
    Content string `json:"content"`
}

type ClaudeRequest struct {
    Model     string          `json:"model"`
    MaxTokens int             `json:"max_tokens"`
    Messages  []ClaudeMessage `json:"messages"`
}

type ClaudeResponse struct {
    Content []struct {
        Text string `json:"text"`
        Type string `json:"type"`
    } `json:"content"`
    Usage struct {
        InputTokens  int `json:"input_tokens"`
        OutputTokens int `json:"output_tokens"`
    } `json:"usage"`
}
```

#### Ollama API Models
```go
type OllamaMessage struct {
    Role    string `json:"role"`    // "user" or "assistant"
    Content string `json:"content"`
}

type OllamaChatRequest struct {
    Model    string          `json:"model"`
    Messages []OllamaMessage `json:"messages"`
    Stream   bool            `json:"stream"`
}

type OllamaChatResponse struct {
    Message OllamaMessage `json:"message"`
    Done    bool          `json:"done"`
}
```

### Configuration Models

#### `config.Config`
```go
type Config struct {
    // API Configuration
    ClaudeAPIKey    string
    ClaudeAPIURL    string
    OpenAIAPIKey    string
    
    // Ollama Configuration
    OllamaURL       string
    OllamaModel     string
    
    // Memory Configuration
    MemoryEnabled       bool
    MemoryDataDir       string
    MemoryRetentionDays int
    
    // Conversation Settings
    MaxRounds       int
    DelayBetweenMsg time.Duration
    OutputFile      string
}
```

### Utility Models

#### `utils.RetryConfig`
```go
type RetryConfig struct {
    MaxRetries      int
    BaseDelay       time.Duration
    MaxDelay        time.Duration
    BackoffFactor   float64
    RetryableErrors []string
}
```

## Data Flow Relationships

### Session Data Flow
```
Message → Conversation → JSON Export → Markdown Export
```

### Memory Data Flow
```
Message → ConversationMemory → Embedding → Vector Storage → Search Results
```

### API Data Flow
```
Internal Message → API-Specific Request → API Response → Internal Message
```

## Storage Patterns

### File-Based Storage
- **Conversations**: Single JSON file per session
- **Memories**: Individual JSON files per memory (enables parallel access)
- **Exports**: Markdown files with formatted output

### Memory Persistence
- **Retention**: 5-day sliding window
- **Cleanup**: Automatic background cleanup of expired memories
- **Indexing**: File-based with in-memory search during runtime

### State Management
- **Session State**: In-memory during conversation
- **Long-term Memory**: Persistent file storage
- **Configuration**: Environment variables with runtime parsing
