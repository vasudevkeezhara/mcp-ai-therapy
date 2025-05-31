#!/bin/bash

# AI Therapy Setup Validation Script
# This script validates that both components are properly set up

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🔍 AI Therapy Setup Validation${NC}"
echo "Checking that both therapy sessions and MCP integration are properly configured..."
echo

# Track validation results
VALIDATION_PASSED=true

# Function to check and report
check_requirement() {
    local description="$1"
    local command="$2"
    local success_message="$3"
    local failure_message="$4"
    
    echo -n "Checking $description... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $success_message${NC}"
        return 0
    else
        echo -e "${RED}❌ $failure_message${NC}"
        VALIDATION_PASSED=false
        return 1
    fi
}

# Function to check file exists
check_file() {
    local description="$1"
    local file_path="$2"
    local success_message="$3"
    local failure_message="$4"
    
    echo -n "Checking $description... "
    
    if [[ -f "$file_path" ]]; then
        echo -e "${GREEN}✅ $success_message${NC}"
        return 0
    else
        echo -e "${RED}❌ $failure_message${NC}"
        VALIDATION_PASSED=false
        return 1
    fi
}

# Function to check directory exists and has content
check_directory() {
    local description="$1"
    local dir_path="$2"
    local success_message="$3"
    local failure_message="$4"
    
    echo -n "Checking $description... "
    
    if [[ -d "$dir_path" ]] && [[ -n "$(ls -A "$dir_path" 2>/dev/null)" ]]; then
        echo -e "${GREEN}✅ $success_message${NC}"
        return 0
    else
        echo -e "${RED}❌ $failure_message${NC}"
        VALIDATION_PASSED=false
        return 1
    fi
}

echo -e "${YELLOW}📋 Part 1: Basic Requirements${NC}"

# Check Go installation
check_requirement "Go installation" \
    "go version" \
    "Go is installed" \
    "Go is not installed or not in PATH"

# Check Python installation
check_requirement "Python installation" \
    "python --version" \
    "Python is installed" \
    "Python is not installed or not in PATH"

# Check if we're in the right directory
check_file "Project structure" \
    "$PROJECT_DIR/main.go" \
    "Found main.go - in correct project directory" \
    "main.go not found - run this script from the ai-therapy directory"

echo
echo -e "${YELLOW}🧠 Part 2: Therapy Session Components${NC}"

# Check Ollama installation
check_requirement "Ollama installation" \
    "which ollama" \
    "Ollama is installed" \
    "Ollama is not installed - run 'brew install ollama'"

# Check if Ollama is running
check_requirement "Ollama service" \
    "curl -s http://localhost:11434/api/tags" \
    "Ollama is running" \
    "Ollama is not running - run 'ollama serve'"

# Check if Ollama has models
echo -n "Checking Ollama models... "
if ollama list 2>/dev/null | grep -q "llama"; then
    echo -e "${GREEN}✅ Ollama models available${NC}"
else
    echo -e "${RED}❌ No Ollama models found - run 'ollama pull llama2'${NC}"
    VALIDATION_PASSED=false
fi

# Check API keys
echo -n "Checking Claude API key... "
if [[ -n "$CLAUDE_API_KEY" ]]; then
    echo -e "${GREEN}✅ Claude API key is set${NC}"
else
    echo -e "${RED}❌ CLAUDE_API_KEY environment variable not set${NC}"
    VALIDATION_PASSED=false
fi

echo -n "Checking OpenAI API key... "
if [[ -n "$OPENAI_API_KEY" ]]; then
    echo -e "${GREEN}✅ OpenAI API key is set${NC}"
else
    echo -e "${YELLOW}⚠️  OpenAI API key not set (optional - will use keyword search)${NC}"
fi

# Check Go dependencies
echo -n "Checking Go dependencies... "
cd "$PROJECT_DIR"
if go mod verify > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Go dependencies are valid${NC}"
else
    echo -e "${RED}❌ Go dependencies issue - run 'go mod tidy'${NC}"
    VALIDATION_PASSED=false
fi

echo
echo -e "${YELLOW}🔗 Part 3: MCP Integration Components${NC}"

# Check Python dependencies
echo -n "Checking Python MCP dependencies... "
cd "$PROJECT_DIR/mcp-server"
if python -c "import mcp" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ MCP Python package is installed${NC}"
else
    echo -e "${RED}❌ MCP package not installed - run 'pip install -r requirements.txt'${NC}"
    VALIDATION_PASSED=false
fi

# Check if memory files exist
check_directory "Therapy memory files" \
    "$PROJECT_DIR/memory_data" \
    "Memory files found - therapy sessions have been run" \
    "No memory files found - run a therapy session first"

# Check Claude Desktop config
CLAUDE_CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    CLAUDE_CONFIG_PATH="$APPDATA/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CLAUDE_CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
fi

check_file "Claude Desktop config" \
    "$CLAUDE_CONFIG_PATH" \
    "Claude Desktop config file exists" \
    "Claude Desktop config not found - copy from claude-config/"

# Validate Claude Desktop config syntax
if [[ -f "$CLAUDE_CONFIG_PATH" ]]; then
    echo -n "Checking Claude Desktop config syntax... "
    if python -m json.tool "$CLAUDE_CONFIG_PATH" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Config syntax is valid${NC}"
    else
        echo -e "${RED}❌ Config syntax is invalid - check JSON format${NC}"
        VALIDATION_PASSED=false
    fi
    
    # Check if config contains ai-therapy-memory server
    echo -n "Checking MCP server configuration... "
    if grep -q "ai-therapy-memory" "$CLAUDE_CONFIG_PATH"; then
        echo -e "${GREEN}✅ AI Therapy MCP server is configured${NC}"
    else
        echo -e "${RED}❌ AI Therapy MCP server not found in config${NC}"
        VALIDATION_PASSED=false
    fi
fi

echo
echo -e "${YELLOW}🧪 Part 4: Functional Tests${NC}"

# Test MCP server
echo -n "Testing MCP server functionality... "
cd "$PROJECT_DIR/mcp-server"
if python test_mcp_server.py > /dev/null 2>&1; then
    echo -e "${GREEN}✅ MCP server tests pass${NC}"
else
    echo -e "${RED}❌ MCP server tests fail - check logs${NC}"
    VALIDATION_PASSED=false
fi

echo
echo -e "${BLUE}📊 Validation Summary${NC}"

if $VALIDATION_PASSED; then
    echo -e "${GREEN}🎉 All validations passed! Your AI Therapy setup is ready.${NC}"
    echo
    echo -e "${BLUE}🚀 Next steps:${NC}"
    echo "1. Run a therapy session: go run main.go"
    echo "2. Restart Claude Desktop to load the MCP server"
    echo "3. Test enhanced Claude by asking about therapeutic insights"
    echo "4. Set up automated scheduling: ./scripts/schedule-therapy.sh"
else
    echo -e "${RED}❌ Some validations failed. Please address the issues above.${NC}"
    echo
    echo -e "${BLUE}🔧 Common fixes:${NC}"
    echo "• Install missing dependencies"
    echo "• Set required environment variables"
    echo "• Run 'ollama serve' to start Ollama"
    echo "• Run 'go mod tidy' to fix Go dependencies"
    echo "• Run 'pip install -r requirements.txt' in mcp-server/"
    echo "• Copy and configure Claude Desktop config file"
    exit 1
fi

echo
echo -e "${YELLOW}💡 Pro tips:${NC}"
echo "• Add API keys to your shell profile for persistence"
echo "• Use 'ollama pull llama3' for better therapy conversations"
echo "• Check logs in logs/ directory for troubleshooting"
echo "• Run this validation script anytime to check your setup"
