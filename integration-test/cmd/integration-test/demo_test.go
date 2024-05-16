//go:build integration

package test

import (
	"encoding/json"
	"fmt"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"io"
	"math/rand"
	"net/http"
	"os"
	"testing"
	"time"
)

type RepositoryDetails struct {
	Id        int    `json:"id"`
	Name      string `json:"name"`
	OwnerId   int    `json:"owner_id"`
	Payload   string `json:"payload"`
	UpdatedAt string `json:"updated_at"`
	CreatedAt string `json:"created_at"`
}

const expectedPayload = `{"clone_url":"https://github.com/huberts90/go-link-scraper.git","description":"Link scraper in Go","id":"80272654","name":"link-scraper"}`

func TestSignRequest(t *testing.T) {
	// Wait for dependencies to be ready
	// It should be managed by wait-for.sh script at the docker-compose level
	time.Sleep(3 * time.Second)

	repoName := fmt.Sprintf("integration-%d", rand.Int())
	apiURL := os.Getenv("API_URL")
	if apiURL == "" {
		panic("API_URL not set")
	}

	resp, err := http.Get(fmt.Sprintf("%s/repositories/demo_tester/%s", apiURL, repoName))
	require.Nil(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	require.Nil(t, err)

	var details RepositoryDetails
	err = json.Unmarshal(body, &details)
	require.Nil(t, err)

	assert.Equal(t, repoName, details.Name)
	assert.Equal(t, expectedPayload, details.Payload)
}
