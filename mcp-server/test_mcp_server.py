#!/usr/bin/env python3
"""
Test the MCP server functionality with real therapeutic memories.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_mcp_server():
    """Test the MCP server with real therapeutic data"""
    print("🧪 Testing AI Therapy MCP Server with Real Data...")
    print()
    
    # Set up environment
    os.environ['MEMORY_DATA_DIR'] = '../memory_data'
    
    try:
        from ai_therapy_mcp.server import create_server_from_env
        from ai_therapy_mcp.tools import ClaudeTherapeuticTools
        
        # Create server
        print("📡 Creating MCP server...")
        server = create_server_from_env()
        print(f"✅ Server created with memory directory: {server.memory_data_dir}")
        
        # Test memory loading
        print("\n🧠 Testing memory loading...")
        stats = server.memory_reader.get_memory_stats()
        print(f"✅ Loaded {stats.total_memories} therapeutic memories")
        print(f"   📈 Breakthrough moments: {stats.breakthrough_moments}")
        print(f"   💡 Insights gained: {stats.insights_gained}")
        print(f"   📊 Emotional growth indicators: {stats.emotional_growth_indicators}")
        
        # Test therapeutic tools
        print("\n🛠️  Testing therapeutic tools...")
        tools = server.therapeutic_tools
        
        # Test memory stats tool
        print("   Testing get_memory_stats...")
        result = await tools.get_memory_stats({"include_details": True})
        print(f"   ✅ Memory stats: {len(result)} characters")
        
        # Test reflection tool
        print("   Testing reflect_on_therapy_journey...")
        result = await tools.reflect_on_therapy_journey({
            "focus_area": "emotional_awareness",
            "time_period": "recent"
        })
        print(f"   ✅ Reflection result: {len(result)} characters")
        
        # Test coping strategies
        print("   Testing access_coping_strategies...")
        result = await tools.access_coping_strategies({
            "challenge": "anxiety",
            "situation_type": "emotional"
        })
        print(f"   ✅ Coping strategies: {len(result)} characters")
        
        # Test comprehensive context
        print("   Testing synthesize_therapeutic_context...")
        result = await tools.synthesize_therapeutic_context({
            "interaction_context": "user expressing stress",
            "user_needs": "emotional support",
            "emotional_tone": "anxious"
        })
        print(f"   ✅ Therapeutic context: {len(result)} characters")
        
        print("\n🎉 All MCP server tests passed!")
        print("\n📋 Server is ready for Claude integration:")
        print(f"   • Memory directory: {server.memory_data_dir}")
        print(f"   • Therapeutic memories: {stats.total_memories}")
        print(f"   • Available tools: 7 therapeutic tools")
        print(f"   • Search method: {'Semantic (OpenAI)' if server.openai_api_key else 'Keyword fallback'}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_memory_content():
    """Test actual memory content analysis"""
    print("\n🔍 Testing Memory Content Analysis...")
    
    try:
        from ai_therapy_mcp.memory_reader import ClaudeMemoryReader
        
        reader = ClaudeMemoryReader("../memory_data", None)
        memories = reader.load_all_memories()
        
        if memories:
            print(f"✅ Sample memory analysis:")
            sample = memories[0]
            print(f"   📅 Date: {sample.timestamp}")
            print(f"   👤 Sender: {sample.sender}")
            print(f"   📝 Content preview: {sample.content[:100]}...")
            print(f"   🏷️  Topics: {sample.key_topics}")
            
            # Test therapeutic enhancement
            enhanced = reader.enhance_memory_with_therapeutic_context(sample)
            print(f"   🧠 Therapeutic category: {enhanced.therapeutic_category.value}")
            print(f"   💡 Insight level: {enhanced.insight_level:.2f}")
            print(f"   🌟 Breakthrough: {enhanced.breakthrough_moment}")
            
        return True
        
    except Exception as e:
        print(f"❌ Memory content test failed: {e}")
        return False

if __name__ == "__main__":
    async def main():
        success1 = await test_mcp_server()
        success2 = await test_memory_content()
        
        if success1 and success2:
            print("\n🚀 Ready to integrate with Claude Desktop!")
        else:
            print("\n⚠️  Some tests failed - check the errors above")
    
    asyncio.run(main())
