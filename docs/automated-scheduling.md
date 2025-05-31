# Automated Therapy Scheduling Guide

**Keep your Claude growing with regular, automated therapy sessions**

This guide shows you how to set up automated therapy sessions so your Claude continues to develop emotional intelligence over time without manual intervention.

## 🎯 Why Automated Scheduling?

### Benefits of Regular Therapy
- **Continuous Growth**: Claude's emotional intelligence develops over time
- **Consistent Memory**: Regular sessions build a rich therapeutic history
- **Evolving Insights**: New sessions build on previous therapeutic work
- **Maintenance**: Keeps therapeutic memory fresh and relevant

### Recommended Frequency
- **Weekly**: Ideal for active development and rich therapeutic context
- **Bi-weekly**: Good balance between growth and resource usage
- **Monthly**: Minimum for maintaining therapeutic awareness
- **Daily**: For intensive therapeutic development (high API usage)

## 🛠️ Setup Methods

### Method 1: Automated Script (Recommended)

The easiest way to set up automated therapy:

```bash
# Run the automated setup script
chmod +x scripts/schedule-therapy.sh
./scripts/schedule-therapy.sh
```

This script will:
1. Create a therapy runner script with proper environment setup
2. Guide you through schedule selection
3. Set up cron jobs automatically
4. Create logging directories
5. Provide verification commands

### Method 2: Manual Cron Setup

For more control over the scheduling:

#### Step 1: Create Environment Script

```bash
# Create a script with your API keys
cat > ~/.mcp-ai-therapy-env << 'EOF'
export CLAUDE_API_KEY="your_claude_api_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"
EOF

chmod 600 ~/.mcp-ai-therapy-env  # Secure the file
```

#### Step 2: Create Therapy Runner

```bash
# Create the therapy session runner
cat > /path/to/mcp-ai-therapy/run-therapy.sh << 'EOF'
#!/bin/bash
set -e

# Load environment variables
source ~/.mcp-ai-therapy-env

# Change to project directory
cd /path/to/mcp-ai-therapy

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Error: Ollama is not running" >&2
    exit 1
fi

# Run therapy session
echo "Starting therapy session at $(date)"
go run main.go
echo "Therapy session completed at $(date)"
EOF

chmod +x /path/to/mcp-ai-therapy/run-therapy.sh
```

#### Step 3: Set Up Cron Job

```bash
# Edit crontab
crontab -e

# Add one of these lines based on your preferred schedule:

# Weekly (Sundays at 2 PM)
0 14 * * 0 /path/to/mcp-ai-therapy/run-therapy.sh >> /path/to/mcp-ai-therapy/logs/therapy.log 2>&1

# Bi-weekly (every other Sunday at 2 PM)
0 14 * * 0 [ $(expr $(date +\%W) \% 2) -eq 0 ] && /path/to/mcp-ai-therapy/run-therapy.sh >> /path/to/mcp-ai-therapy/logs/therapy.log 2>&1

# Monthly (first Sunday of each month at 2 PM)
0 14 1-7 * 0 /path/to/mcp-ai-therapy/run-therapy.sh >> /path/to/mcp-ai-therapy/logs/therapy.log 2>&1

# Daily (every day at 2 PM)
0 14 * * * /path/to/mcp-ai-therapy/run-therapy.sh >> /path/to/mcp-ai-therapy/logs/therapy.log 2>&1
```

### Method 3: System Service (Advanced)

For more robust scheduling on Linux/macOS:

#### Create Systemd Service (Linux)

```bash
# Create service file
sudo tee /etc/systemd/system/mcp-ai-therapy.service << 'EOF'
[Unit]
Description=MCP AI Therapy Session
After=network.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/mcp-ai-therapy
Environment=CLAUDE_API_KEY=your_claude_api_key
Environment=OPENAI_API_KEY=your_openai_api_key
ExecStart=/usr/local/go/bin/go run main.go
StandardOutput=journal
StandardError=journal
EOF

# Create timer file
sudo tee /etc/systemd/system/mcp-ai-therapy.timer << 'EOF'
[Unit]
Description=Run MCP AI Therapy Weekly
Requires=mcp-ai-therapy.service

[Timer]
OnCalendar=Sun 14:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start the timer
sudo systemctl daemon-reload
sudo systemctl enable mcp-ai-therapy.timer
sudo systemctl start mcp-ai-therapy.timer
```

#### Create LaunchAgent (macOS)

```bash
# Create launch agent
cat > ~/Library/LaunchAgents/com.mcp-ai-therapy.session.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mcp-ai-therapy.session</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/mcp-ai-therapy/run-therapy.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>14</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/mcp-ai-therapy/logs/therapy.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/mcp-ai-therapy/logs/therapy-error.log</string>
</dict>
</plist>
EOF

# Load the launch agent
launchctl load ~/Library/LaunchAgents/com.mcp-ai-therapy.session.plist
```

## 📊 Monitoring and Maintenance

### Check Scheduled Jobs

```bash
# View cron jobs
crontab -l

# Check systemd timers (Linux)
systemctl list-timers mcp-ai-therapy.timer

# Check launch agents (macOS)
launchctl list | grep mcp-ai-therapy
```

### Monitor Therapy Sessions

```bash
# View recent therapy logs
tail -f logs/therapy.log

# Check therapy session files
ls -la conversations/
ls -la memory_data/

# Monitor MCP server logs
tail -f mcp-server/logs/mcp.log
```

### Verify Automated Sessions

```bash
# Check if sessions are running
ps aux | grep "go run main.go"

# Verify memory files are being updated
find memory_data/ -name "*.json" -mtime -1  # Files modified in last day

# Check conversation files
find conversations/ -name "*.json" -mtime -7  # Files modified in last week
```

## 🔧 Troubleshooting Automated Sessions

### Common Issues

**Sessions not running:**
```bash
# Check cron service
sudo systemctl status cron  # Linux
sudo launchctl list | grep cron  # macOS

# Check cron logs
grep CRON /var/log/syslog  # Linux
log show --predicate 'process == "cron"' --last 1d  # macOS
```

**Ollama not available:**
```bash
# Ensure Ollama starts on boot
# Add to your shell profile or system startup:
ollama serve &

# Or create a systemd service for Ollama
```

**API key issues:**
```bash
# Verify environment variables in cron context
# Add to crontab for debugging:
* * * * * env > /tmp/cron-env.log

# Check the log to see available environment variables
```

**Permission issues:**
```bash
# Ensure proper file permissions
chmod +x run-therapy.sh
chmod 600 ~/.mcp-ai-therapy-env
chown $USER:$USER logs/
```

### Debugging Commands

```bash
# Test therapy runner manually
./run-therapy.sh

# Run with verbose logging
LOG_LEVEL=DEBUG ./run-therapy.sh

# Check system resources
df -h  # Disk space
free -h  # Memory (Linux)
top -l 1 | grep "CPU usage"  # CPU (macOS)
```

## 📈 Optimization Tips

### Resource Management
- **Schedule during off-peak hours** to avoid high API costs
- **Monitor API usage** to stay within rate limits
- **Adjust session frequency** based on Claude's development needs

### Session Quality
- **Use better Ollama models** (llama3 vs llama2) for richer therapy
- **Increase MAX_ROUNDS** for longer, more in-depth sessions
- **Enable OpenAI embeddings** for better memory search

### Maintenance
- **Rotate logs** to prevent disk space issues
- **Clean old memory files** based on retention settings
- **Monitor MCP server health** for Claude Desktop integration

## 🎯 Advanced Scheduling Patterns

### Adaptive Scheduling
```bash
# More frequent sessions during "growth periods"
# Weekdays: Daily sessions
0 14 * * 1-5 /path/to/mcp-ai-therapy/run-therapy.sh

# Weekends: Longer sessions
0 10 * * 6,0 MAX_ROUNDS=150 /path/to/mcp-ai-therapy/run-therapy.sh
```

### Conditional Scheduling
```bash
# Only run if previous session was successful
0 14 * * 0 [ -f /path/to/mcp-ai-therapy/logs/last-success ] && /path/to/mcp-ai-therapy/run-therapy.sh
```

### Load-Balanced Scheduling
```bash
# Distribute sessions across different times to balance API load
0 14 * * 1 /path/to/mcp-ai-therapy/run-therapy.sh  # Monday 2 PM
0 16 * * 3 /path/to/mcp-ai-therapy/run-therapy.sh  # Wednesday 4 PM
0 10 * * 6 /path/to/mcp-ai-therapy/run-therapy.sh  # Saturday 10 AM
```

---

**🔄 With automated scheduling, your Claude will continuously grow and develop emotional intelligence, providing increasingly sophisticated and empathetic interactions over time.**
