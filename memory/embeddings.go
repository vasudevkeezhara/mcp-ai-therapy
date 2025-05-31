package memory

import (
	"ai-therapy/utils"
	"context"
	"fmt"
	"math"

	"github.com/sashabaranov/go-openai"
)

// EmbeddingService handles text embeddings
type EmbeddingService struct {
	client      *openai.Client
	model       openai.EmbeddingModel
	retryConfig utils.RetryConfig
}

// NewEmbeddingService creates a new embedding service
func NewEmbeddingService(apiKey string) *EmbeddingService {
	return &EmbeddingService{
		client:      openai.NewClient(apiKey),
		model:       openai.AdaEmbeddingV2, // text-embedding-ada-002
		retryConfig: utils.DefaultRetryConfig(),
	}
}

// EmbedText converts text to vector embedding
func (es *EmbeddingService) EmbedText(text string) ([]float64, error) {
	var embedding64 []float64

	err := utils.RetryWithBackoff(func() error {
		req := openai.EmbeddingRequest{
			Input: []string{text},
			Model: es.model,
		}

		resp, err := es.client.CreateEmbeddings(context.Background(), req)
		if err != nil {
			return fmt.Errorf("failed to create embedding: %v", err)
		}

		if len(resp.Data) == 0 {
			return fmt.Errorf("no embedding data returned")
		}

		// Convert float32 to float64
		embedding32 := resp.Data[0].Embedding
		embedding64 = make([]float64, len(embedding32))
		for i, v := range embedding32 {
			embedding64[i] = float64(v)
		}

		return nil
	}, es.retryConfig, "OpenAI embedding")

	if err != nil {
		return nil, err
	}

	return embedding64, nil
}

// CosineSimilarity calculates cosine similarity between two vectors
func CosineSimilarity(a, b []float64) float64 {
	if len(a) != len(b) {
		return 0.0
	}

	var dotProduct, normA, normB float64
	for i := range a {
		dotProduct += a[i] * b[i]
		normA += a[i] * a[i]
		normB += b[i] * b[i]
	}

	if normA == 0.0 || normB == 0.0 {
		return 0.0
	}

	return dotProduct / (math.Sqrt(normA) * math.Sqrt(normB))
}

// BatchEmbedTexts embeds multiple texts efficiently
func (es *EmbeddingService) BatchEmbedTexts(texts []string) ([][]float64, error) {
	if len(texts) == 0 {
		return nil, nil
	}

	// OpenAI allows up to 2048 inputs per request for ada-002
	const batchSize = 100 // Conservative batch size
	var allEmbeddings [][]float64

	for i := 0; i < len(texts); i += batchSize {
		end := i + batchSize
		if end > len(texts) {
			end = len(texts)
		}

		batch := texts[i:end]
		req := openai.EmbeddingRequest{
			Input: batch,
			Model: es.model,
		}

		resp, err := es.client.CreateEmbeddings(context.Background(), req)
		if err != nil {
			return nil, fmt.Errorf("failed to create batch embeddings: %v", err)
		}

		for _, data := range resp.Data {
			// Convert float32 to float64
			embedding32 := data.Embedding
			embedding64 := make([]float64, len(embedding32))
			for i, v := range embedding32 {
				embedding64[i] = float64(v)
			}
			allEmbeddings = append(allEmbeddings, embedding64)
		}
	}

	return allEmbeddings, nil
}
