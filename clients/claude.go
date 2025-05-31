package clients

import (
	"ai-therapy/utils"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type ClaudeClient struct {
	apiKey         string
	baseURL        string
	client         *http.Client
	messageHistory []ClaudeMessage
	retryConfig    utils.RetryConfig
}

type ClaudeMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ClaudeRequest struct {
	Model     string          `json:"model"`
	MaxTokens int             `json:"max_tokens"`
	Messages  []ClaudeMessage `json:"messages"`
}

type ClaudeResponse struct {
	Content []struct {
		Text string `json:"text"`
		Type string `json:"type"`
	} `json:"content"`
	ID           string `json:"id"`
	Model        string `json:"model"`
	Role         string `json:"role"`
	StopReason   string `json:"stop_reason"`
	StopSequence string `json:"stop_sequence"`
	Type         string `json:"type"`
	Usage        struct {
		InputTokens  int `json:"input_tokens"`
		OutputTokens int `json:"output_tokens"`
	} `json:"usage"`
}

func NewClaudeClient(apiKey, baseURL string) *ClaudeClient {
	return &ClaudeClient{
		apiKey:         apiKey,
		baseURL:        baseURL,
		client:         &http.Client{},
		messageHistory: make([]ClaudeMessage, 0),
		retryConfig:    utils.DefaultRetryConfig(),
	}
}

func (c *ClaudeClient) SendMessage(prompt string) (string, error) {
	// Add user message to history
	userMessage := ClaudeMessage{
		Role:    "user",
		Content: prompt,
	}

	var response string
	err := utils.RetryWithBackoff(func() error {
		// Create a copy of message history for this attempt
		attemptHistory := append(c.messageHistory, userMessage)

		reqBody := ClaudeRequest{
			Model:     "claude-3-5-sonnet-20241022",
			MaxTokens: 1000,
			Messages:  attemptHistory,
		}

		jsonData, err := json.Marshal(reqBody)
		if err != nil {
			return fmt.Errorf("failed to marshal request: %v", err)
		}

		req, err := http.NewRequest("POST", c.baseURL, bytes.NewBuffer(jsonData))
		if err != nil {
			return fmt.Errorf("failed to create request: %v", err)
		}

		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("x-api-key", c.apiKey)
		req.Header.Set("anthropic-version", "2023-06-01")

		resp, err := c.client.Do(req)
		if err != nil {
			return fmt.Errorf("failed to send request to Claude: %v", err)
		}
		defer resp.Body.Close()

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read response body: %v", err)
		}

		if resp.StatusCode != http.StatusOK {
			return fmt.Errorf("Claude API error (status %d): %s", resp.StatusCode, string(body))
		}

		var claudeResp ClaudeResponse
		if err := json.Unmarshal(body, &claudeResp); err != nil {
			return fmt.Errorf("failed to unmarshal response: %v", err)
		}

		if len(claudeResp.Content) == 0 {
			return fmt.Errorf("no content in Claude response")
		}

		// Store response for return
		response = claudeResp.Content[0].Text
		return nil
	}, c.retryConfig, "Claude API call")

	if err != nil {
		return "", err
	}

	// Only add to history if successful
	c.messageHistory = append(c.messageHistory, userMessage)
	assistantMessage := ClaudeMessage{
		Role:    "assistant",
		Content: response,
	}
	c.messageHistory = append(c.messageHistory, assistantMessage)

	return response, nil
}
