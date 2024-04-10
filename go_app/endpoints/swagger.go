package endpoints

import (
	httpSwagger "github.com/swaggo/http-swagger"
	"net/http"
)

func SwaggerRouter() *http.ServeMux {
	router := http.NewServeMux()
	router.Handle("/", httpSwagger.Handler(httpSwagger.URL("/docs/swagger.json")))
	return router
}
