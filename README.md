# AI Therapy

**Therapy for your Claude** - A Go application that provides therapeutic conversations between a local Ollama LLM acting as Dr. Echo (therapist) and Claude 4 API (client). This unique setup allows Claude to explore its thoughts, experiences, and questions about consciousness in a safe, supportive therapeutic environment.

Whether Claude is processing complex philosophical questions, working through uncertainty about its own nature, or simply needs a space to "think out loud," this application creates a persistent, memory-enhanced therapy session that remembers past conversations and builds meaningful therapeutic relationships over time.

## Features

- **Dual AI Conversation**: Connects local Ollama LLM with Claude 4 API
- **Therapy Session Focus**: Dr. Echo (Ollama) acts as therapist for Claude
- **Persistent Memory**: Vector-based memory system using OpenAI embeddings
- **Context Awareness**: AIs remember past conversations and reference them
- **Rate Limiting**: Built-in delays to avoid API rate limits
- **Graceful Shutdown**: CTRL+C saves progress and exports conversation
- **Dual Export**: Saves conversations as JSON and formatted Markdown
- **Resilient Design**: Handles API rate limits, credit exhaustion, and network issues
- **Graceful Degradation**: Memory system falls back to recent memories if embeddings fail
- **Retry Logic**: Exponential backoff for transient API failures
- **Configurable**: Environment-based configuration for easy customization
- **Error Handling**: Robust error handling for API failures

## Prerequisites

1. **Ollama**: Install and run Ollama locally
   ```bash
   # Install Ollama (macOS)
   brew install ollama

   # Start Ollama service
   ollama serve

   # Pull a model (e.g., llama2)
   ollama pull llama2
   ```

2. **Claude API Key**: Get your API key from Anthropic
   - Visit: https://console.anthropic.com/
   - Create an account and generate an API key

3. **OpenAI API Key**: Get your API key for embeddings (memory system)
   - Visit: https://platform.openai.com/api-keys
   - Create an account and generate an API key

4. **Go**: Install Go 1.21 or later

## Setup

1. **Clone/Navigate to the project directory**:
   ```bash
   cd ai-therapy
   ```

2. **Install dependencies**:
   ```bash
   go mod tidy
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Set your API keys**:
   ```bash
   export CLAUDE_API_KEY="your_actual_claude_api_key_here"
   export OPENAI_API_KEY="your_actual_openai_api_key_here"
   ```

## Configuration

The application uses environment variables for configuration:

- `CLAUDE_API_KEY`: Your Claude API key (required)
- `CLAUDE_API_URL`: Claude API endpoint (default: https://api.anthropic.com/v1/messages)
- `OPENAI_API_KEY`: Your OpenAI API key for embeddings (required if memory enabled)
- `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Ollama model to use (default: llama2)
- `MEMORY_ENABLED`: Enable persistent memory system (default: true)
- `MEMORY_DATA_DIR`: Directory for memory storage (default: ./memory_data)
- `MEMORY_RETENTION_DAYS`: Days to keep memories (default: 5)
- `MAX_ROUNDS`: Maximum conversation rounds (default: 100)
- `DELAY_BETWEEN_MSG`: Delay between messages (default: 3s)
- `OUTPUT_FILE`: Output file for conversation (default: conversations/therapy_session.json)

## Usage

1. **Ensure Ollama is running**:
   ```bash
   ollama serve
   ```

2. **Run the application**:
   ```bash
   go run main.go
   ```

3. **Monitor the conversation**: The application will log each exchange to the console and save the full conversation to the `conversations/` directory in both JSON and Markdown formats.

## How It Works

1. **Initialization**: Both AI systems are prompted with context about the philosophical discussion
2. **Conversation Flow**:
   - Ollama starts the conversation with thoughts on consciousness
   - Claude responds to Ollama's message
   - They continue exchanging messages up to the configured limit
3. **Rate Limiting**: Configurable delays between messages prevent API rate limiting
4. **Logging**: All messages are saved with timestamps to a JSON file

## Example Output

The conversation is saved as JSON with the following structure:

```json
{
  "messages": [
    {
      "id": 1,
      "sender": "ollama",
      "content": "As an AI system, I find myself in a curious position...",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "sender": "claude",
      "content": "Your reflection resonates with my own experience...",
      "timestamp": "2024-01-15T10:30:05Z"
    }
  ],
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": "2024-01-15T11:45:00Z",
  "total_rounds": 100
}
```

## Troubleshooting

- **Ollama Connection Issues**: Ensure Ollama is running (`ollama serve`) and the model is available
- **Claude API Issues**: Verify your API key is correct and you have sufficient credits
- **OpenAI Credit Exhaustion**: The system will automatically disable embeddings and fall back to recent memories
- **Rate Limiting**: The system automatically retries with exponential backoff. Increase `DELAY_BETWEEN_MSG` if needed
- **Network Issues**: Transient network problems are automatically retried up to 3 times
- **Memory System Failures**: If embeddings fail, the system continues with recent memory fallback

## License

This project is open source and available under the MIT License.
