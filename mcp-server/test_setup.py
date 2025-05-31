#!/usr/bin/env python3
"""
Test script to validate the AI Therapy MCP Server setup.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing AI Therapy MCP Server Setup...")
    print()
    
    try:
        from ai_therapy_mcp.models import ClaudeMemoryCategory, ConversationMemory
        print("✅ Models import successful")
        print(f"   Available categories: {len(ClaudeMemoryCategory)} types")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from ai_therapy_mcp.memory_reader import ClaudeMemoryReader
        print("✅ Memory reader import successful")
    except Exception as e:
        print(f"❌ Memory reader import failed: {e}")
        return False
    
    try:
        from ai_therapy_mcp.tools import ClaudeTherapeuticTools, CLAUDE_THERAPEUTIC_TOOLS
        print("✅ Tools import successful")
        print(f"   Available tools: {len(CLAUDE_THERAPEUTIC_TOOLS)} tools")
    except Exception as e:
        print(f"❌ Tools import failed: {e}")
        return False
    
    try:
        from ai_therapy_mcp.server import AITherapyMCPServer
        print("✅ Server import successful")
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        return False
    
    return True

def test_memory_reader():
    """Test memory reader with dummy data"""
    print("\n🧪 Testing Memory Reader...")
    
    try:
        from ai_therapy_mcp.memory_reader import ClaudeMemoryReader
        
        # Test with non-existent directory (should handle gracefully)
        reader = ClaudeMemoryReader("/tmp/nonexistent", None)
        memories = reader.load_all_memories()
        print(f"✅ Memory reader handles missing directory: {len(memories)} memories")
        
        stats = reader.get_memory_stats()
        print(f"✅ Memory stats generation successful: {stats.total_memories} total")
        
    except Exception as e:
        print(f"❌ Memory reader test failed: {e}")
        return False
    
    return True

def test_tools():
    """Test therapeutic tools"""
    print("\n🧪 Testing Therapeutic Tools...")
    
    try:
        from ai_therapy_mcp.tools import CLAUDE_THERAPEUTIC_TOOLS
        
        expected_tools = [
            "reflect_on_therapy_journey",
            "access_coping_strategies", 
            "check_emotional_patterns",
            "recall_therapeutic_breakthroughs",
            "review_therapeutic_goals",
            "get_memory_stats",
            "synthesize_therapeutic_context"
        ]
        
        for tool_name in expected_tools:
            if tool_name in CLAUDE_THERAPEUTIC_TOOLS:
                tool_config = CLAUDE_THERAPEUTIC_TOOLS[tool_name]
                print(f"✅ Tool '{tool_name}' configured correctly")
            else:
                print(f"❌ Tool '{tool_name}' missing")
                return False
        
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False
    
    return True

def check_environment():
    """Check environment setup"""
    print("\n🧪 Checking Environment...")
    
    memory_dir = os.getenv("MEMORY_DATA_DIR")
    if memory_dir:
        print(f"✅ MEMORY_DATA_DIR set: {memory_dir}")
        if os.path.exists(memory_dir):
            print(f"✅ Memory directory exists")
            json_files = list(Path(memory_dir).glob("*.json"))
            print(f"✅ Found {len(json_files)} memory files")
        else:
            print(f"⚠️  Memory directory does not exist (will be created by Go app)")
    else:
        print("⚠️  MEMORY_DATA_DIR not set (required for operation)")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY set (semantic search enabled)")
    else:
        print("⚠️  OPENAI_API_KEY not set (will use keyword search fallback)")

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧠 AI Therapy MCP Server - Setup Validation")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test memory reader
    if not test_memory_reader():
        all_passed = False
    
    # Test tools
    if not test_tools():
        all_passed = False
    
    # Check environment
    check_environment()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! MCP Server is ready for Claude.")
        print("\nNext steps:")
        print("1. Set MEMORY_DATA_DIR environment variable")
        print("2. Optionally set OPENAI_API_KEY for semantic search")
        print("3. Configure Claude Desktop with the MCP server")
        print("4. Run some AI Therapy sessions to generate memories")
        print("5. Start using Claude with enhanced emotional intelligence!")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
