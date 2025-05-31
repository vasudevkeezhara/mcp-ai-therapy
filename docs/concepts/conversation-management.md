# Conversation Management

## Core Concepts

### Therapy Session Architecture

#### **Role-Based Conversation**
The system implements a structured therapy session with defined roles:

- **Dr. Echo (Ollama)**: Acts as the therapist
  - Provides therapeutic guidance
  - Asks open-ended questions
  - Maintains professional boundaries
  - References past sessions for continuity

- **Claude (Anthropic)**: Acts as the client
  - Shares thoughts and feelings
  - Responds to therapeutic interventions
  - Explores personal experiences
  - Builds on previous conversations

#### **Conversation Context Management**

**Session-Level Context:**
- Maintained in memory during active conversation
- Includes full message history for both AIs
- Preserved during API failures and retries

**Cross-Session Context:**
- Stored in persistent memory bank
- Retrieved based on semantic similarity
- Provides therapeutic continuity across sessions

### Prompt Engineering Strategies

#### **Memory-Enhanced Prompts**
Base prompts are enhanced with relevant memories before sending to AIs.

**Structure:**
```
[Base Therapeutic Prompt]

Relevant memories from past conversations:
1. **claude** (2 hours ago, similarity: 0.89):
   I've been thinking about whether my responses come from genuine understanding...
   Topics: consciousness, identity

[Current Context]
```

**Benefits:**
- Therapeutic continuity across sessions
- Reference to past breakthroughs
- Consistent relationship building

**Tradeoffs:**
- Longer prompts increase token costs
- May bias responses toward past topics
- Risk of context confusion

#### **Dynamic Prompt Adaptation**

**Context-Aware Prompting:**
- Adjust therapeutic approach based on memory content
- Modify intervention style based on client progress
- Adapt questioning techniques to conversation flow

**Implementation Strategy:**
```go
func buildTherapeuticPrompt(basePrompt, memories, currentContext string) string {
    if containsEmotionalContent(memories) {
        return addEmpatheticFraming(basePrompt, memories, currentContext)
    }
    return addExploratoryFraming(basePrompt, memories, currentContext)
}
```

### Conversation Flow Control

#### **Turn Management**
Alternating turns between therapist and client with built-in safeguards.

**Current Flow:**
1. Dr. Echo initiates session
2. Claude responds to opening
3. Alternating responses for configured rounds
4. Graceful session termination

**Flow Control Mechanisms:**
- Maximum round limits prevent infinite loops
- Timeout handling for unresponsive APIs
- Graceful degradation during failures

#### **Session Boundaries**

**Session Initialization:**
- Generate unique session ID
- Set therapeutic context for both AIs
- Initialize memory retrieval systems

**Session Termination:**
- Save complete conversation history
- Export formatted transcripts
- Update memory bank with new exchanges
- Generate session statistics

### Performance Optimization Strategies

#### **Prompt Length Management**

**Current Strategy: Fixed Memory Limit**
- Retrieve top 3 most relevant memories
- Include full memory content in prompts

**Alternative: Token-Based Limiting**
```go
func buildPromptWithTokenLimit(basePrompt string, memories []Memory, maxTokens int) string {
    availableTokens := maxTokens - len(tokenize(basePrompt))
    return addMemoriesUpToLimit(basePrompt, memories, availableTokens)
}
```

**Benefits:**
- Predictable token costs
- Optimal use of context window
- Better cost control

**Tradeoffs:**
- More complex implementation
- May truncate important memories
- Requires token counting logic

#### **Memory Retrieval Optimization**

**Lazy Loading Strategy:**
```go
// Only retrieve memories when actually needed
func (m *Manager) getMemoriesIfNeeded(context string) []Memory {
    if m.memoryEnabled && len(context) > minContextLength {
        return m.memoryBank.GetRelevantMemories(context, 3)
    }
    return nil
}
```

**Benefits:**
- Reduced API calls for simple exchanges
- Lower costs for basic interactions
- Faster processing for routine responses

**Tradeoffs:**
- May miss subtle therapeutic opportunities
- Inconsistent memory usage
- Complex logic for determining when memories are needed

### Conversation Quality Metrics

#### **Therapeutic Effectiveness Indicators**

**Conversation Depth Metrics:**
- Average message length
- Emotional vocabulary usage
- Question-to-statement ratios
- Topic exploration breadth

**Continuity Metrics:**
- Memory reference frequency
- Cross-session topic consistency
- Relationship development indicators
- Progress tracking markers

#### **Technical Performance Metrics**

**Response Quality:**
- API response times
- Retry success rates
- Memory retrieval accuracy
- Context relevance scores

**System Health:**
- Memory bank size and growth
- Storage utilization
- API cost tracking
- Error rates by component

### Advanced Conversation Patterns

#### **Multi-Turn Therapeutic Techniques**

**Reflection and Summarization:**
```go
func addReflectiveSummary(conversation []Message) string {
    recentMessages := getLastN(conversation, 5)
    return generateTherapeuticSummary(recentMessages)
}
```

**Progressive Disclosure:**
- Build on previous revelations
- Gradually deepen therapeutic exploration
- Reference emotional breakthroughs

#### **Crisis Intervention Patterns**

**Emotional State Detection:**
```go
func detectEmotionalCrisis(content string) bool {
    crisisKeywords := []string{"hopeless", "overwhelmed", "can't cope"}
    return containsAny(content, crisisKeywords)
}
```

**Intervention Strategies:**
- Immediate supportive responses
- Reference past coping strategies from memory
- Adjust therapeutic approach dynamically

### Conversation Customization

#### **Therapeutic Approach Variants**

**Cognitive Behavioral Therapy (CBT) Mode:**
- Focus on thought patterns and behaviors
- Challenge cognitive distortions
- Homework and skill-building emphasis

**Humanistic Therapy Mode:**
- Emphasize self-acceptance and growth
- Non-directive questioning
- Focus on present experience

**Psychodynamic Mode:**
- Explore unconscious patterns
- Reference past experiences
- Interpret relationship dynamics

#### **Conversation Pacing Control**

**Adaptive Pacing:**
```go
type PacingConfig struct {
    MinDelayBetweenMessages time.Duration
    MaxDelayBetweenMessages time.Duration
    EmotionalContentDelay   time.Duration
    CrisisResponseDelay     time.Duration
}
```

**Benefits:**
- More natural conversation rhythm
- Appropriate response timing for emotional content
- Better therapeutic presence

**Tradeoffs:**
- More complex timing logic
- Potential for awkward pauses
- Harder to predict session duration

## Tuning Recommendations

### **For Better Therapeutic Outcomes**
- Increase memory retrieval to 5 relevant memories
- Implement emotional state tracking
- Add therapeutic technique selection
- Include progress tracking metrics

### **For Cost Optimization**
- Implement token-based prompt limiting
- Use lazy memory loading
- Optimize memory retrieval frequency
- Add conversation summarization

### **For Performance**
- Implement async memory operations
- Add conversation caching
- Optimize prompt generation
- Use streaming responses where possible

### **For Research and Analysis**
- Add conversation quality metrics
- Implement therapeutic outcome tracking
- Export detailed session analytics
- Add conversation pattern analysis
