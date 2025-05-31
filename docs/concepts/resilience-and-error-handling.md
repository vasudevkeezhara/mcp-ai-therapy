# Resilience and Error Handling

## Core Resilience Concepts

### Retry Logic with Exponential Backoff

#### **Exponential Backoff Strategy**
Delays between retries increase exponentially to avoid overwhelming failing services.

**Formula**: `delay = baseDelay * (backoffFactor ^ attempt)`

**Current Configuration:**
- Base Delay: 2 seconds
- Backoff Factor: 2.0
- Max Retries: 3
- Max Delay: 2 minutes

**Retry Sequence:**
1. First attempt: Immediate
2. First retry: 2 seconds delay
3. Second retry: 4 seconds delay  
4. Third retry: 8 seconds delay
5. Give up: Return error

#### **Error Classification**

**Retryable Errors:**
- Rate limiting (429 status)
- Server errors (500, 502, 503, 504)
- Network timeouts
- Connection failures

**Non-Retryable Errors:**
- Authentication failures (401, 403)
- Credit exhaustion
- Invalid requests (400)
- Not found (404)

### Graceful Degradation

#### **Memory System Degradation**
When OpenAI embeddings fail, the system automatically falls back to simpler approaches.

**Degradation Hierarchy:**
1. **Vector Embeddings** (highest quality)
   - Semantic similarity search
   - Cosine similarity scoring
   
2. **Recent Memory Fallback** (medium quality)
   - Timestamp-based sorting
   - Recency-weighted scoring
   
3. **No Memory** (basic functionality)
   - Continue conversation without context
   - Maintain session state only

#### **API Failure Handling**

**Claude API Failure:**
- Retry with exponential backoff
- Log detailed error information
- Continue with Ollama if possible
- Save conversation state

**Ollama API Failure:**
- Retry connection attempts
- Check if service is running
- Provide clear error messages
- Maintain conversation history

**OpenAI API Failure:**
- Detect credit exhaustion vs temporary issues
- Disable embeddings permanently if credits exhausted
- Fall back to recent memory search
- Continue therapy session uninterrupted

## Performance vs Reliability Tradeoffs

### **Retry Configuration Tuning**

#### **Aggressive Retries (High Reliability)**
```go
RetryConfig{
    MaxRetries:    5,
    BaseDelay:     1 * time.Second,
    MaxDelay:      5 * time.Minute,
    BackoffFactor: 1.5,
}
```

**Benefits:**
- Higher success rate for transient failures
- Better user experience during network issues
- More resilient to temporary service outages

**Tradeoffs:**
- Longer wait times for permanent failures
- Higher resource usage
- May mask underlying service issues

#### **Conservative Retries (Fast Failure)**
```go
RetryConfig{
    MaxRetries:    1,
    BaseDelay:     5 * time.Second,
    MaxDelay:      30 * time.Second,
    BackoffFactor: 2.0,
}
```

**Benefits:**
- Faster failure detection
- Lower resource usage
- Clearer error reporting

**Tradeoffs:**
- More failures during temporary issues
- Less resilient to network hiccups
- May give up too quickly

### **Memory Fallback Strategies**

#### **Aggressive Memory Retention**
Keep more memories and use looser similarity thresholds.

**Configuration:**
- Retention: 14 days
- Similarity threshold: 0.5
- Memory limit per query: 10

**Benefits:**
- Richer therapeutic context
- Better long-term relationship building
- More comprehensive memory recall

**Tradeoffs:**
- Higher storage costs
- Longer prompt processing
- Potential context confusion

#### **Conservative Memory Usage**
Minimal memory with strict relevance filtering.

**Configuration:**
- Retention: 2 days
- Similarity threshold: 0.8
- Memory limit per query: 2

**Benefits:**
- Lower costs and storage
- Faster processing
- More focused context

**Tradeoffs:**
- Limited therapeutic continuity
- May miss important connections
- Less relationship depth

## Error Recovery Patterns

### **Circuit Breaker Pattern**
Temporarily disable failing services to prevent cascade failures.

**Implementation Strategy:**
```go
type CircuitBreaker struct {
    failureCount    int
    lastFailureTime time.Time
    threshold       int
    timeout         time.Duration
    state          State // CLOSED, OPEN, HALF_OPEN
}
```

**Benefits:**
- Prevents resource exhaustion
- Faster failure detection
- Automatic recovery attempts

**Tradeoffs:**
- May disable working services prematurely
- Adds complexity to error handling
- Requires careful threshold tuning

### **Bulkhead Pattern**
Isolate different types of failures to prevent total system failure.

**Current Implementation:**
- Memory failures don't stop conversation
- API failures are isolated per client
- Storage failures don't affect memory retrieval

**Benefits:**
- Partial functionality during failures
- Better fault isolation
- Improved system availability

### **Timeout Strategies**

#### **Aggressive Timeouts**
Short timeouts for fast failure detection.

**Configuration:**
- API calls: 10 seconds
- Embedding requests: 15 seconds
- File operations: 5 seconds

**Benefits:**
- Quick failure detection
- Better user experience
- Prevents hanging operations

**Tradeoffs:**
- May timeout valid slow operations
- Less tolerance for network latency
- Higher failure rates

#### **Conservative Timeouts**
Longer timeouts for better success rates.

**Configuration:**
- API calls: 60 seconds
- Embedding requests: 120 seconds
- File operations: 30 seconds

**Benefits:**
- Higher success rates
- Better tolerance for slow networks
- Fewer false failures

**Tradeoffs:**
- Slower failure detection
- Potential resource exhaustion
- Poor user experience during actual failures

## Monitoring and Observability

### **Error Metrics to Track**
- Retry success rates by error type
- API response times and failure rates
- Memory system performance metrics
- Credit exhaustion frequency

### **Alerting Strategies**
- High failure rates (>10% over 5 minutes)
- Credit exhaustion warnings
- Memory system degradation
- Unusual error patterns

### **Logging Best Practices**

**Structured Logging:**
```go
log.Printf("API_CALL_FAILED service=%s attempt=%d/%d error=%v", 
    serviceName, attempt, maxRetries, err)
```

**Error Context:**
- Include operation context
- Log retry attempts and outcomes
- Track degradation state changes
- Record recovery events

## Tuning Recommendations

### **For High Availability**
- Increase retry counts and timeouts
- Lower similarity thresholds for memory fallback
- Implement circuit breakers
- Add health checks

### **For Performance**
- Reduce retry counts and timeouts
- Implement aggressive caching
- Use async operations where possible
- Optimize memory retrieval

### **For Cost Optimization**
- Implement smart retry policies (avoid retrying credit exhaustion)
- Use local fallbacks when possible
- Optimize API usage patterns
- Monitor and alert on cost spikes

### **For Development vs Production**

**Development:**
- Shorter timeouts for faster feedback
- More verbose logging
- Aggressive failure modes for testing
- Local fallbacks preferred

**Production:**
- Longer timeouts for reliability
- Structured logging for monitoring
- Conservative failure handling
- Remote services preferred
