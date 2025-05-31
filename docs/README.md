# AI Therapy Documentation

Welcome to the comprehensive documentation for the AI Therapy project. This documentation provides detailed insights into the architecture, concepts, and future development plans for the therapeutic AI conversation system.

## Documentation Structure

### 📐 [Architecture](./architecture/)
Technical architecture and system design documentation.

- **[Overview](./architecture/overview.md)**: High-level system architecture, component interactions, and design principles
- **[Data Models](./architecture/data-models.md)**: Complete data structure definitions and relationships

### 📚 [Glossary](./glossary/)
Reference documentation for files, methods, and components.

- **[Files and Methods](./glossary/files-and-methods.md)**: Comprehensive listing of all files and their major methods (excluding constructors)

### 💡 [Concepts](./concepts/)
In-depth explanations of core concepts and implementation strategies.

- **[Memory and Embeddings](./concepts/memory-and-embeddings.md)**: Vector embeddings, memory architecture, and performance optimization strategies
- **[Resilience and Error Handling](./concepts/resilience-and-error-handling.md)**: Retry logic, graceful degradation, and reliability patterns
- **[Conversation Management](./concepts/conversation-management.md)**: Therapy session flow, prompt engineering, and conversation optimization

### 🚀 [Future Improvements](./future-improvements/)
Roadmap and enhancement plans for the project.

- **[Short-Term](./future-improvements/short-term.md)**: 1-3 month improvements including vector databases, streaming responses, and monitoring
- **[Long-Term](./future-improvements/long-term.md)**: 3-12 month vision including multi-modal memory, adaptive therapy, and scalability

## Quick Navigation

### For Developers
- Start with [Architecture Overview](./architecture/overview.md) to understand the system design
- Review [Files and Methods](./glossary/files-and-methods.md) for implementation details
- Check [Resilience Concepts](./concepts/resilience-and-error-handling.md) for error handling patterns

### For System Administrators
- Read [Resilience and Error Handling](./concepts/resilience-and-error-handling.md) for operational insights
- Review [Short-Term Improvements](./future-improvements/short-term.md) for monitoring and reliability enhancements

### For Researchers
- Explore [Memory and Embeddings](./concepts/memory-and-embeddings.md) for AI memory concepts
- Review [Conversation Management](./concepts/conversation-management.md) for therapy session insights
- Check [Long-Term Improvements](./future-improvements/long-term.md) for research opportunities

### For Product Managers
- Start with [Architecture Overview](./architecture/overview.md) for system capabilities
- Review both [Short-Term](./future-improvements/short-term.md) and [Long-Term](./future-improvements/long-term.md) improvement plans
- Check [Conversation Management](./concepts/conversation-management.md) for user experience insights

## Key System Features

### 🧠 **Intelligent Memory System**
- Vector-based semantic memory with OpenAI embeddings
- 5-day retention with automatic cleanup
- Graceful degradation when embeddings fail
- Cross-session therapeutic continuity

### 🛡️ **Resilient Architecture**
- Exponential backoff retry logic for all APIs
- Credit exhaustion detection and handling
- Graceful shutdown with progress preservation
- Comprehensive error classification and handling

### 💬 **Therapeutic Conversation Management**
- Role-based therapy sessions (Dr. Echo as therapist, Claude as client)
- Memory-enhanced prompts for context continuity
- Dual export (JSON + formatted Markdown)
- Signal handling for graceful interruption

### ⚡ **Performance Optimizations**
- Conversation-level memory granularity
- Similarity-based memory retrieval
- Configurable retry policies
- Efficient storage and cleanup mechanisms

## System Requirements

### Runtime Dependencies
- **Go 1.21+**: Core application runtime
- **Ollama**: Local LLM service
- **OpenAI API**: Embedding generation (optional with graceful degradation)
- **Claude API**: Remote AI conversation partner

### Development Dependencies
- **Git**: Version control
- **Make**: Build automation (optional)
- **Docker**: Containerization (future)

## Configuration Overview

The system is highly configurable through environment variables:

- **API Keys**: Claude and OpenAI API credentials
- **Memory Settings**: Retention period, storage location, embedding preferences
- **Conversation Parameters**: Round limits, delays, output formats
- **Resilience Settings**: Retry policies, timeout configurations

## Getting Started

1. **Read the [Architecture Overview](./architecture/overview.md)** to understand the system design
2. **Review the main [README.md](../README.md)** for setup and installation instructions
3. **Explore [Concepts](./concepts/)** for deeper understanding of key features
4. **Check [Future Improvements](./future-improvements/)** for development roadmap

## Contributing

When contributing to the project:

1. **Update Documentation**: Ensure any new features or changes are reflected in the appropriate documentation files
2. **Follow Patterns**: Use existing architectural patterns and error handling approaches
3. **Test Thoroughly**: Verify resilience features and graceful degradation scenarios
4. **Consider Performance**: Review memory and performance implications of changes

## Documentation Maintenance

This documentation is maintained alongside the codebase. When making changes:

- **Architecture changes**: Update [Architecture](./architecture/) documentation
- **New methods or files**: Update [Glossary](./glossary/) documentation
- **Concept changes**: Update relevant [Concepts](./concepts/) documentation
- **Feature additions**: Update [Future Improvements](./future-improvements/) as appropriate

---

*Last updated: December 2024*
*Documentation version: 1.0*
