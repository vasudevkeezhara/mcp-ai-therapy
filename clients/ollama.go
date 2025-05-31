package clients

import (
	"ai-therapy/utils"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type OllamaClient struct {
	baseURL        string
	model          string
	client         *http.Client
	messageHistory []OllamaMessage
	retryConfig    utils.RetryConfig
}

type OllamaMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type OllamaChatRequest struct {
	Model    string          `json:"model"`
	Messages []OllamaMessage `json:"messages"`
	Stream   bool            `json:"stream"`
}

type OllamaChatResponse struct {
	Message OllamaMessage `json:"message"`
	Done    bool          `json:"done"`
}

func NewOllamaClient(baseURL, model string) *OllamaClient {
	return &OllamaClient{
		baseURL:        baseURL,
		model:          model,
		client:         &http.Client{},
		messageHistory: make([]OllamaMessage, 0),
		retryConfig:    utils.DefaultRetryConfig(),
	}
}

func (c *OllamaClient) SendMessage(prompt string) (string, error) {
	// Add user message to history
	userMessage := OllamaMessage{
		Role:    "user",
		Content: prompt,
	}

	var response string
	err := utils.RetryWithBackoff(func() error {
		// Create a copy of message history for this attempt
		attemptHistory := append(c.messageHistory, userMessage)

		reqBody := OllamaChatRequest{
			Model:    c.model,
			Messages: attemptHistory,
			Stream:   false,
		}

		jsonData, err := json.Marshal(reqBody)
		if err != nil {
			return fmt.Errorf("failed to marshal request: %v", err)
		}

		url := fmt.Sprintf("%s/api/chat", c.baseURL)
		resp, err := c.client.Post(url, "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			return fmt.Errorf("failed to send request to Ollama: %v", err)
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)
			return fmt.Errorf("Ollama API error (status %d): %s", resp.StatusCode, string(body))
		}

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read response body: %v", err)
		}

		var ollamaResp OllamaChatResponse
		if err := json.Unmarshal(body, &ollamaResp); err != nil {
			return fmt.Errorf("failed to unmarshal response: %v", err)
		}

		// Store response for return
		response = ollamaResp.Message.Content
		return nil
	}, c.retryConfig, "Ollama API call")

	if err != nil {
		return "", err
	}

	// Only add to history if successful
	c.messageHistory = append(c.messageHistory, userMessage)
	assistantMessage := OllamaMessage{
		Role:    "assistant",
		Content: response,
	}
	c.messageHistory = append(c.messageHistory, assistantMessage)

	return response, nil
}
