# Architecture Overview

## System Architecture

The AI Consciousness Chat application follows a modular, layered architecture designed for resilience, maintainability, and extensibility.

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Application                     │
│                         (main.go)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Conversation Manager                       │
│                 (conversation/manager.go)                   │
│  • Orchestrates therapy sessions                           │
│  • Manages conversation flow                               │
│  • Handles graceful shutdown                               │
└─────────────┬─────────────────────────┬─────────────────────┘
              │                         │
┌─────────────▼─────────────┐ ┌─────────▼─────────────────────┐
│      API Clients          │ │      Memory System            │
│   (clients/ package)      │ │   (memory/ package)           │
│                           │ │                               │
│ ┌─────────────────────────┐ │ ┌─────────────────────────────┐ │
│ │   Claude Client         │ │ │      Memory Bank            │ │
│ │ • Chat context          │ │ │ • Vector embeddings         │ │
│ │ • Retry logic           │ │ │ • Semantic search           │ │
│ │ • Error handling        │ │ │ • Graceful degradation      │ │
│ └─────────────────────────┘ │ └─────────────────────────────┘ │
│                           │ │                               │
│ ┌─────────────────────────┐ │ ┌─────────────────────────────┐ │
│ │   Ollama Client         │ │ │   Embedding Service         │ │
│ │ • Local LLM interface   │ │ │ • OpenAI API integration    │ │
│ │ • Chat context          │ │ │ • Retry with backoff        │ │
│ │ • Retry logic           │ │ │ • Credit exhaustion detect  │ │
│ └─────────────────────────┘ │ └─────────────────────────────┘ │
└───────────────────────────┘ │                               │
                              │ ┌─────────────────────────────┐ │
                              │ │    Memory Storage           │ │
                              │ │ • JSON file persistence     │ │
                              │ │ • Automatic cleanup         │ │
                              │ │ • 5-day retention           │ │
                              │ └─────────────────────────────┘ │
                              └───────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Utility Layer                            │
│                   (utils/ package)                          │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                  Retry Logic                            │ │
│ │ • Exponential backoff                                   │ │
│ │ • Error classification                                  │ │
│ │ • Credit exhaustion detection                           │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Conversation Initialization
```
main.go → config.Load() → Initialize Clients → Initialize Memory Bank → Start Conversation
```

### 2. Message Exchange Flow
```
User Input → Memory Retrieval → Prompt Enhancement → API Call → Response → Memory Storage → Next Round
```

### 3. Memory System Flow
```
Message → Embedding Generation → Vector Storage → Similarity Search → Context Injection
```

## Key Design Principles

### 1. **Resilience First**
- Every external API call is wrapped with retry logic
- Graceful degradation when services fail
- Automatic fallback mechanisms

### 2. **Separation of Concerns**
- **Clients**: Handle API communication and retry logic
- **Memory**: Manages persistent context and embeddings
- **Conversation**: Orchestrates the therapy session flow
- **Utils**: Provides shared functionality

### 3. **Stateful Context Management**
- Both AI clients maintain conversation history
- Memory bank provides long-term context across sessions
- Session state is preserved during interruptions

### 4. **Configuration-Driven**
- Environment variables control all behavior
- Easy to adjust retry policies, memory settings, etc.
- No hardcoded values in business logic

## Component Interactions

### Memory-Enhanced Conversations
1. **Context Retrieval**: Before each response, relevant memories are retrieved
2. **Prompt Enhancement**: Base prompts are enhanced with memory context
3. **Response Storage**: Each exchange is stored with embeddings for future retrieval

### Error Handling Chain
1. **Retry Layer**: Handles transient failures with exponential backoff
2. **Degradation Layer**: Falls back to alternative approaches
3. **Persistence Layer**: Ensures no data loss during failures

### Graceful Shutdown
1. **Signal Handler**: Catches CTRL+C interruptions
2. **State Preservation**: Saves conversation progress and memories
3. **Export Generation**: Creates both JSON and Markdown outputs
