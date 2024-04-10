package middleware

import (
	"context"
	"database/sql"
	"net/http"
)

func DbMiddleware(next http.Handler, db *sql.DB) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := context.WithValue(r.Context(), "db", db)
		r = r.WithContext(ctx)

		next.ServeHTTP(w, r)
	})
}
