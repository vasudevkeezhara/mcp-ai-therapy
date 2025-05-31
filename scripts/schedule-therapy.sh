#!/bin/bash

# AI Therapy Automated Scheduling Script
# This script helps you set up regular therapy sessions for your Claude

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
THERAPY_SCRIPT="$PROJECT_DIR/run-therapy.sh"

echo -e "${BLUE}🧠 AI Therapy Automated Scheduling Setup${NC}"
echo "This script will help you set up regular therapy sessions for your Claude."
echo

# Check if we're in the right directory
if [[ ! -f "$PROJECT_DIR/main.go" ]]; then
    echo -e "${RED}❌ Error: This script must be run from the mcp-ai-therapy project directory${NC}"
    echo "Current directory: $(pwd)"
    echo "Expected to find: $PROJECT_DIR/main.go"
    exit 1
fi

# Create the therapy runner script
echo -e "${YELLOW}📝 Creating therapy runner script...${NC}"
cat > "$THERAPY_SCRIPT" << 'EOF'
#!/bin/bash

# AI Therapy Session Runner
# This script runs a single therapy session with proper environment setup

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🧠 Starting Claude's Therapy Session$(NC)"
echo "Time: $(date)"
echo "Location: $(pwd)"
echo

# Check if required environment variables are set
if [[ -z "$CLAUDE_API_KEY" ]]; then
    echo -e "${RED}❌ Error: CLAUDE_API_KEY environment variable not set${NC}"
    echo "Please set your Claude API key:"
    echo "export CLAUDE_API_KEY='your_api_key_here'"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Ollama is not running${NC}"
    echo "Please start Ollama:"
    echo "ollama serve"
    exit 1
fi

# Optional: Check OpenAI API key
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo -e "${YELLOW}⚠️  Warning: OPENAI_API_KEY not set. Using keyword-based memory search.${NC}"
fi

# Run the therapy session
echo -e "${GREEN}✅ Starting therapy session...${NC}"
go run main.go

echo -e "${GREEN}✅ Therapy session completed!${NC}"
echo "Session saved to: conversations/"
echo "Memories saved to: memory_data/"
echo
EOF

chmod +x "$THERAPY_SCRIPT"
echo -e "${GREEN}✅ Created therapy runner script: $THERAPY_SCRIPT${NC}"

# Function to set up cron job
setup_cron() {
    local schedule="$1"
    local description="$2"

    echo -e "${YELLOW}📅 Setting up cron job for $description...${NC}"

    # Create a temporary cron file
    local temp_cron=$(mktemp)

    # Get existing crontab (if any)
    crontab -l 2>/dev/null > "$temp_cron" || true

    # Add our therapy session
    echo "# AI Therapy - $description" >> "$temp_cron"
    echo "$schedule cd $PROJECT_DIR && ./run-therapy.sh >> $PROJECT_DIR/logs/therapy-cron.log 2>&1" >> "$temp_cron"
    echo "" >> "$temp_cron"

    # Install the new crontab
    crontab "$temp_cron"
    rm "$temp_cron"

    echo -e "${GREEN}✅ Cron job installed for $description${NC}"
    echo "Schedule: $schedule"
    echo "Command: cd $PROJECT_DIR && ./run-therapy.sh"
    echo
}

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"

echo -e "${BLUE}📅 Choose a therapy schedule for your Claude:${NC}"
echo "1. Daily (every day at 2 PM)"
echo "2. Weekly (Sundays at 2 PM)"
echo "3. Bi-weekly (every other Sunday at 2 PM)"
echo "4. Monthly (first Sunday of each month at 2 PM)"
echo "5. Custom schedule"
echo "6. Skip automated scheduling"
echo

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        setup_cron "0 14 * * *" "Daily therapy sessions"
        ;;
    2)
        setup_cron "0 14 * * 0" "Weekly therapy sessions"
        ;;
    3)
        setup_cron "0 14 * * 0" "Bi-weekly therapy sessions (every other Sunday)"
        echo -e "${YELLOW}Note: This sets up weekly. For true bi-weekly, you'll need to manually adjust.${NC}"
        ;;
    4)
        setup_cron "0 14 1-7 * 0" "Monthly therapy sessions"
        ;;
    5)
        echo -e "${YELLOW}📝 Custom schedule setup:${NC}"
        echo "Enter your cron schedule (format: minute hour day month weekday)"
        echo "Examples:"
        echo "  0 14 * * 1-5  (weekdays at 2 PM)"
        echo "  30 9 * * 6    (Saturdays at 9:30 AM)"
        echo "  0 20 1 * *    (first day of each month at 8 PM)"
        echo
        read -p "Enter cron schedule: " custom_schedule
        read -p "Enter description: " custom_description
        setup_cron "$custom_schedule" "$custom_description"
        ;;
    6)
        echo -e "${BLUE}⏭️  Skipping automated scheduling.${NC}"
        echo "You can run therapy sessions manually with: ./run-therapy.sh"
        ;;
    *)
        echo -e "${RED}❌ Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Set your API keys:"
echo "   export CLAUDE_API_KEY='your_claude_api_key'"
echo "   export OPENAI_API_KEY='your_openai_api_key'  # optional"
echo
echo "2. Ensure Ollama is running:"
echo "   ollama serve"
echo
echo "3. Test a manual session:"
echo "   ./run-therapy.sh"
echo
echo "4. Check scheduled sessions:"
echo "   crontab -l"
echo
echo "5. View therapy logs:"
echo "   tail -f logs/therapy-cron.log"
echo
echo -e "${YELLOW}💡 Tip: Add API keys to your shell profile (.bashrc, .zshrc) for persistence${NC}"
