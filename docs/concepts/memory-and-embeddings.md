# Memory and Vector Embeddings

## Core Concepts

### Vector Embeddings
Vector embeddings are numerical representations of text that capture semantic meaning. Each piece of text is converted into a high-dimensional vector (1536 dimensions for OpenAI's ada-002 model) where similar meanings result in similar vectors.

**Key Properties:**
- **Semantic Similarity**: "I feel anxious" and "I'm worried" have similar vectors
- **Mathematical Operations**: Can calculate similarity using cosine similarity
- **Language Agnostic**: Captures meaning beyond exact word matches

### Memory Architecture

#### **Conversation-Level Granularity**
Each AI message is stored as a separate memory unit rather than entire sessions.

**Benefits:**
- **Precise Retrieval**: Find specific exchanges, not entire conversations
- **Better Context**: Mix relevant moments from different sessions
- **Efficient Storage**: Only store what's actually relevant

**Tradeoffs:**
- **More Storage**: Each message requires separate embedding
- **Processing Overhead**: More API calls to OpenAI

#### **Shared Memory Bank**
Both AIs access the same memory repository.

**Benefits:**
- **Therapeutic Continuity**: Dr. Echo remembers what Claude shared previously
- **Relationship Building**: Both AIs can reference shared experiences
- **Context Coherence**: Consistent understanding of conversation history

**Tradeoffs:**
- **Privacy Concerns**: No separation between AI-specific memories
- **Context Pollution**: One AI's memories might confuse the other

## Performance Optimization Strategies

### **Embedding Optimization**

#### **Batch Processing**
```go
// Instead of individual calls
embedding1 := EmbedText("message 1")
embedding2 := EmbedText("message 2")

// Use batch processing
embeddings := BatchEmbedTexts([]string{"message 1", "message 2"})
```

**Benefits:**
- **Cost Reduction**: Fewer API calls to OpenAI
- **Speed Improvement**: Parallel processing
- **Rate Limit Efficiency**: Better API quota utilization

**Tradeoffs:**
- **Memory Usage**: Larger requests require more RAM
- **Error Handling**: Batch failures affect multiple items

#### **Embedding Caching**
Store embeddings locally to avoid regenerating identical content.

**Implementation Strategy:**
```go
type EmbeddingCache struct {
    cache map[string][]float64  // text -> embedding
    maxSize int
}
```

**Benefits:**
- **Cost Savings**: No duplicate OpenAI API calls
- **Speed**: Instant retrieval for repeated content
- **Offline Capability**: Works without internet for cached items

**Tradeoffs:**
- **Memory Usage**: Cache grows over time
- **Staleness**: Embeddings don't update if model changes

### **Search Optimization**

#### **Similarity Threshold Tuning**
Current threshold: 0.7 (70% similarity)

**Higher Threshold (0.8-0.9):**
- **Pros**: More precise matches, less noise
- **Cons**: Might miss relevant but loosely related memories

**Lower Threshold (0.5-0.6):**
- **Pros**: More comprehensive context, catches subtle connections
- **Cons**: May include irrelevant memories, longer prompts

#### **Memory Ranking Strategies**

**Current: Pure Similarity**
```go
sort.Slice(results, func(i, j int) bool {
    return results[i].Similarity > results[j].Similarity
})
```

**Alternative: Weighted Scoring**
```go
score := similarity * 0.7 + recency * 0.2 + importance * 0.1
```

**Benefits:**
- **Balanced Results**: Mix of relevant and recent memories
- **Therapeutic Value**: Prioritize breakthrough moments

**Tradeoffs:**
- **Complexity**: More parameters to tune
- **Subjectivity**: "Importance" is hard to quantify

### **Storage Optimization**

#### **Memory Compression**
Reduce storage size for large memory banks.

**Strategies:**
- **Summary-Only Storage**: Store summaries instead of full content
- **Embedding Quantization**: Reduce vector precision (float64 → float32)
- **Compression**: Gzip JSON files

**Tradeoffs:**
- **Information Loss**: Compressed data loses detail
- **Processing Overhead**: Compression/decompression costs
- **Compatibility**: May break with existing data

#### **Retention Policies**

**Current: Time-Based (5 days)**
```go
cutoff := time.Now().Add(-retentionPeriod)
```

**Alternative: Importance-Based**
```go
// Keep memories with high therapeutic value longer
if memory.Importance > threshold {
    extendRetention(memory)
}
```

**Alternative: Usage-Based**
```go
// Keep frequently accessed memories
if memory.AccessCount > threshold {
    extendRetention(memory)
}
```

## Graceful Degradation Strategies

### **Embedding Failure Fallback**

#### **Recent Memory Fallback**
When embeddings fail, fall back to timestamp-based retrieval.

**Current Implementation:**
```go
if !embeddingEnabled {
    return getRecentMemories(memories, limit)
}
```

**Alternative: Keyword Matching**
```go
func getKeywordMemories(memories []Memory, keywords []string) []Memory {
    // Simple text matching when embeddings unavailable
}
```

#### **Hybrid Approaches**
Combine multiple fallback strategies:

1. **Try Embeddings** (best quality)
2. **Fall back to Keywords** (medium quality)
3. **Fall back to Recent** (basic continuity)

### **Performance vs Quality Tradeoffs**

#### **Memory Retrieval Limit**
Current: 3 memories per query

**Higher Limit (5-10):**
- **Pros**: Richer context, better therapeutic continuity
- **Cons**: Longer prompts, higher token costs, potential confusion

**Lower Limit (1-2):**
- **Pros**: Focused context, faster processing, lower costs
- **Cons**: May miss important connections

#### **Embedding Model Selection**

**OpenAI ada-002 (Current)**
- **Pros**: High quality, 1536 dimensions, good semantic understanding
- **Cons**: Costs money, requires internet, rate limited

**Local Alternatives (sentence-transformers)**
- **Pros**: Free, offline, no rate limits
- **Cons**: Lower quality, requires local ML setup

**Hybrid Approach**
- Use local embeddings for development/testing
- Use OpenAI for production quality

## Tuning Recommendations

### **For Better Therapeutic Continuity**
- Increase memory retrieval limit to 5
- Lower similarity threshold to 0.6
- Implement importance-based retention
- Add emotional state tracking

### **For Cost Optimization**
- Implement embedding caching
- Use batch processing for multiple memories
- Consider local embedding models for development
- Reduce memory retention period

### **For Performance**
- Add memory indexing (vector database)
- Implement async memory storage
- Use memory compression
- Add memory access patterns optimization
