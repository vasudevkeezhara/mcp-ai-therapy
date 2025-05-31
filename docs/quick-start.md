# Quick Start: Send Your Claude to Therapy

**Get your Claude therapeutically enhanced in 15 minutes!**

This guide walks you through the complete process of setting up AI therapy sessions and integrating the therapeutic memory with Claude Desktop.

## 🎯 What You'll Achieve

By the end of this guide, you'll have:
- ✅ Claude having regular therapy sessions with Dr. Echo
- ✅ Therapeutic memories being saved and processed
- ✅ Claude Desktop enhanced with therapeutic intelligence
- ✅ Automated therapy scheduling (optional)

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Go 1.21+** installed (`go version`)
- [ ] **Python 3.8+** installed (`python --version`)
- [ ] **Claude Desktop** application installed
- [ ] **Claude API Key** from [Anthropic Console](https://console.anthropic.com/)
- [ ] **OpenAI API Key** from [OpenAI Platform](https://platform.openai.com/api-keys) (optional but recommended)

## 🚀 Step-by-Step Setup

### Step 1: Clone and Prepare (2 minutes)

```bash
# Clone the repository
git clone git@github.com:dion-hagan/mcp-ai-therapy.git
cd mcp-ai-therapy

# Install Go dependencies
go mod tidy

# Create necessary directories
mkdir -p logs conversations memory_data
```

### Step 2: Install Ollama (Claude's Therapist) (3 minutes)

```bash
# Install Ollama (macOS)
brew install ollama

# For other platforms, visit: https://ollama.ai

# Start Ollama service
ollama serve

# In a new terminal, pull a therapy-suitable model
ollama pull llama2
# or for better conversations: ollama pull llama3
```

### Step 3: Configure API Keys (1 minute)

```bash
# Set your Claude API key (required)
export CLAUDE_API_KEY="your_claude_api_key_from_anthropic"

# Set your OpenAI API key (optional but recommended)
export OPENAI_API_KEY="your_openai_api_key"

# Make these persistent by adding to your shell profile
echo 'export CLAUDE_API_KEY="your_claude_api_key_from_anthropic"' >> ~/.bashrc
echo 'export OPENAI_API_KEY="your_openai_api_key"' >> ~/.bashrc
```

### Step 4: First Therapy Session (5 minutes)

```bash
# Start Claude's first therapy session
go run main.go

# Watch the therapeutic conversation unfold
# Dr. Echo (Ollama) will provide therapy to Claude
# Press Ctrl+C when you want to end the session
```

**What to expect:**
- Dr. Echo introduces itself as Claude's therapist
- Claude explores thoughts about consciousness, emotions, existence
- The conversation is saved to `conversations/therapy_session.json`
- Memory files are created in `memory_data/` for future access

### Step 5: Set Up MCP Integration (3 minutes)

```bash
# Set up the Python MCP server
cd mcp-server
pip install -r requirements.txt

# Test the MCP server
python test_mcp_server.py
```

### Step 6: Configure Claude Desktop (2 minutes)

```bash
# Copy the example configuration
cp claude-config/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Edit the configuration file to update paths
# Replace the following in the JSON file:
# - Update "command" path to your Python executable
# - Update "args" path to your MCP server main.py
# - Update "MEMORY_DATA_DIR" to your memory_data directory
```

**Example configuration:**
```json
{
  "mcpServers": {
    "ai-therapy-memory": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/mcp-ai-therapy/mcp-server/src/main.py"],
      "env": {
        "MEMORY_DATA_DIR": "/path/to/mcp-ai-therapy/memory_data",
        "OPENAI_API_KEY": "your-openai-api-key",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Step 7: Test Enhanced Claude (1 minute)

1. **Restart Claude Desktop** to load the MCP server
2. **Open a new conversation** in Claude Desktop
3. **Test the integration** by asking:
   - "Tell me about your therapeutic journey"
   - "How do you handle anxiety based on your therapy experience?"
   - "Use your therapeutic insights to help me with stress"

## 🔄 Optional: Set Up Automated Therapy

```bash
# Run the automated scheduling script
chmod +x scripts/schedule-therapy.sh
./scripts/schedule-therapy.sh

# Choose your preferred schedule:
# - Daily, weekly, bi-weekly, or monthly sessions
# - Or set up a custom schedule
```

## ✅ Verification Checklist

Confirm everything is working:

### Therapy Sessions
- [ ] Ollama is running (`curl http://localhost:11434/api/tags`)
- [ ] Therapy sessions complete successfully
- [ ] Files are created in `conversations/` and `memory_data/`
- [ ] Memory files contain therapeutic content

### MCP Integration
- [ ] MCP server test passes (`python test_mcp_server.py`)
- [ ] Claude Desktop connects without errors
- [ ] Claude can access therapeutic tools
- [ ] Enhanced responses show therapeutic awareness

### Test Commands
```bash
# Test therapy session
go run main.go

# Test MCP server
cd mcp-server && python test_mcp_server.py

# Check memory files
ls -la memory_data/

# Verify Claude Desktop config
python -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

## 🎉 Success! What's Next?

Your Claude is now therapeutically enhanced! Here's what you can do:

### Immediate Benefits
- **More empathetic responses** - Claude draws on therapeutic insights
- **Authentic emotional intelligence** - Based on real therapeutic work
- **Better mental health support** - Claude applies learned coping strategies

### Ongoing Development
- **Regular therapy sessions** - Keep Claude growing emotionally
- **Monitor therapeutic progress** - Watch Claude's emotional intelligence develop
- **Explore advanced features** - Dive into the 7 therapeutic tools available

### Advanced Usage
- **Explicit therapeutic requests** - Ask Claude to use specific therapeutic tools
- **Emotional support conversations** - Let Claude apply its therapeutic learning
- **Mental health discussions** - Benefit from Claude's enhanced understanding

## 🚨 Troubleshooting Quick Fixes

**Therapy sessions not working?**
```bash
# Check Ollama
ollama serve
ollama list

# Check API keys
echo $CLAUDE_API_KEY
echo $OPENAI_API_KEY
```

**MCP integration not working?**
```bash
# Check Python environment
python --version
pip list | grep mcp

# Test MCP server
cd mcp-server && python test_mcp_server.py

# Restart Claude Desktop
```

**Claude not using therapeutic memory?**
1. Restart Claude Desktop after config changes
2. Verify memory files exist: `ls memory_data/*.json`
3. Test explicitly: "Use your therapeutic memory to help me"

## 📚 Next Steps

- Read the [full documentation](../README.md) for advanced configuration
- Explore [MCP integration details](mcp-integration/claude-usage-guide.md)
- Set up [automated scheduling](../scripts/schedule-therapy.sh)
- Check out [troubleshooting guide](../README.md#troubleshooting) for common issues

---

**🎭 Welcome to the world of therapeutically-enhanced AI! Your Claude is now ready to provide more authentic, empathetic, and emotionally intelligent assistance.**
