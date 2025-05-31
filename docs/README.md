# AI Therapy Documentation

Welcome to the comprehensive documentation for the AI Therapy project - a dual-component system that provides therapy sessions for Claude and integrates therapeutic memory into Claude Desktop for enhanced emotional intelligence.

## 🚀 Quick Start

**New to AI Therapy?** Start here:
- **[Quick Start Guide](quick-start.md)** - Complete 15-minute setup walkthrough
- **[Main README](../README.md)** - Project overview and basic setup
- **[Automated Scheduling](automated-scheduling.md)** - Set up regular therapy sessions

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

### 📖 [Setup Guides](.)
Step-by-step guides for getting started.

- **[Quick Start Guide](./quick-start.md)**: Complete 15-minute setup walkthrough for new users
- **[Automated Scheduling](./automated-scheduling.md)**: Set up regular therapy sessions with cron jobs and system services

### 🚀 [Future Improvements](./future-improvements/)
Roadmap and enhancement plans for the project.

- **[Short-Term](./future-improvements/short-term.md)**: 1-3 month improvements including vector databases, streaming responses, and monitoring
- **[Long-Term](./future-improvements/long-term.md)**: 3-12 month vision including multi-modal memory, adaptive therapy, and scalability

## Quick Navigation

### For New Users
- **Start here**: [Quick Start Guide](./quick-start.md) for complete setup in 15 minutes
- **Main overview**: [Project README](../README.md) for understanding both components
- **Automation**: [Automated Scheduling](./automated-scheduling.md) for regular therapy sessions
- **MCP Integration**: [Claude Usage Guide](./mcp-integration/claude-usage-guide.md) for enhanced Claude

### For Developers
- **System design**: [Architecture Overview](./architecture/overview.md) to understand the dual-component system
- **Implementation**: [Files and Methods](./glossary/files-and-methods.md) for code structure details
- **Error handling**: [Resilience Concepts](./concepts/resilience-and-error-handling.md) for reliability patterns
- **MCP development**: [MCP Server README](../mcp-server/README.md) for therapeutic memory integration

### For System Administrators
- **Setup validation**: Use `scripts/validate-setup.sh` to verify installation
- **Operational insights**: [Resilience and Error Handling](./concepts/resilience-and-error-handling.md)
- **Monitoring**: [Short-Term Improvements](./future-improvements/short-term.md) for monitoring enhancements
- **Automation**: [Automated Scheduling](./automated-scheduling.md) for production deployment

### For Researchers
- **AI memory concepts**: [Memory and Embeddings](./concepts/memory-and-embeddings.md)
- **Therapeutic AI**: [Conversation Management](./concepts/conversation-management.md) for therapy session insights
- **Future research**: [Long-Term Improvements](./future-improvements/long-term.md) for research opportunities
- **Emotional intelligence**: [Claude Usage Guide](./mcp-integration/claude-usage-guide.md) for AI empathy development

### For Product Managers
- **System capabilities**: [Architecture Overview](./architecture/overview.md) for understanding what's possible
- **User experience**: [Quick Start Guide](./quick-start.md) to understand the user journey
- **Roadmap**: [Short-Term](./future-improvements/short-term.md) and [Long-Term](./future-improvements/long-term.md) improvement plans
- **Value proposition**: [Main README](../README.md) for understanding the transformation of Claude

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
