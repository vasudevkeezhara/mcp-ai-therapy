package utils

import (
	"fmt"
	"log"
	"math"
	"strings"
	"time"
)

// RetryConfig defines retry behavior
type RetryConfig struct {
	MaxRetries      int
	BaseDelay       time.Duration
	MaxDelay        time.Duration
	BackoffFactor   float64
	RetryableErrors []string
}

// DefaultRetryConfig returns sensible defaults for API retries
func DefaultRetryConfig() RetryConfig {
	return RetryConfig{
		MaxRetries:    3,
		BaseDelay:     time.Second * 2,
		MaxDelay:      time.Minute * 2,
		BackoffFactor: 2.0,
		RetryableErrors: []string{
			"rate limit",
			"rate_limit",
			"429",
			"500",
			"502",
			"503",
			"504",
			"timeout",
			"connection",
			"network",
		},
	}
}

// IsRetryableError checks if an error should trigger a retry
func (rc RetryConfig) IsRetryableError(err error) bool {
	if err == nil {
		return false
	}
	
	errStr := strings.ToLower(err.Error())
	for _, retryableErr := range rc.RetryableErrors {
		if strings.Contains(errStr, retryableErr) {
			return true
		}
	}
	return false
}

// IsCreditExhaustedError checks if error indicates no credits/quota
func IsCreditExhaustedError(err error) bool {
	if err == nil {
		return false
	}
	
	errStr := strings.ToLower(err.Error())
	creditErrors := []string{
		"insufficient_quota",
		"quota_exceeded",
		"billing",
		"payment",
		"credit",
		"usage limit",
		"exceeded your current quota",
		"insufficient funds",
	}
	
	for _, creditErr := range creditErrors {
		if strings.Contains(errStr, creditErr) {
			return true
		}
	}
	return false
}

// CalculateDelay calculates exponential backoff delay
func (rc RetryConfig) CalculateDelay(attempt int) time.Duration {
	if attempt <= 0 {
		return rc.BaseDelay
	}
	
	delay := float64(rc.BaseDelay) * math.Pow(rc.BackoffFactor, float64(attempt-1))
	if delay > float64(rc.MaxDelay) {
		delay = float64(rc.MaxDelay)
	}
	
	return time.Duration(delay)
}

// RetryWithBackoff executes a function with exponential backoff
func RetryWithBackoff(operation func() error, config RetryConfig, operationName string) error {
	var lastErr error
	
	for attempt := 0; attempt <= config.MaxRetries; attempt++ {
		if attempt > 0 {
			delay := config.CalculateDelay(attempt)
			log.Printf("Retrying %s (attempt %d/%d) after %v delay...", 
				operationName, attempt, config.MaxRetries, delay)
			time.Sleep(delay)
		}
		
		err := operation()
		if err == nil {
			if attempt > 0 {
				log.Printf("✓ %s succeeded after %d retries", operationName, attempt)
			}
			return nil
		}
		
		lastErr = err
		
		// Check if this is a credit exhaustion error (don't retry)
		if IsCreditExhaustedError(err) {
			log.Printf("⚠️  Credit exhaustion detected for %s: %v", operationName, err)
			return fmt.Errorf("credits exhausted: %v", err)
		}
		
		// Check if this error is retryable
		if !config.IsRetryableError(err) {
			log.Printf("⚠️  Non-retryable error for %s: %v", operationName, err)
			return err
		}
		
		log.Printf("⚠️  Retryable error for %s (attempt %d/%d): %v", 
			operationName, attempt+1, config.MaxRetries+1, err)
	}
	
	return fmt.Errorf("operation %s failed after %d retries: %v", 
		operationName, config.MaxRetries, lastErr)
}
