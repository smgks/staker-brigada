package middleware

import (
	"encoding/json"
	"log"
	"net/http"
)

type ErrorResponse struct {
	Error   bool   `json:"error"`
	Message string `json:"message"`
}

func ResponseWrapperMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		defer func() {
			if err := recover(); err != nil {
				log.Printf("Recovered from panic: %v", err)
				w.WriteHeader(http.StatusInternalServerError)
				response := ErrorResponse{
					Error:   true,
					Message: "Internal Server Error",
				}
				_ = json.NewEncoder(w).Encode(response)
			}
		}()
		next.ServeHTTP(w, r) // Call the next handler
	})
}
