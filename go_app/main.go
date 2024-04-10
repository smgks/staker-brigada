package main

import (
	"brigadaServer/database"
	"brigadaServer/endpoints"
	"brigadaServer/middleware"
	"brigadaServer/utils"
	"database/sql"
	httpSwagger "github.com/swaggo/http-swagger"
	"gopkg.in/ini.v1"
	"log"
	"net/http"
)

func main() {
	log.Println("START")
	cfg, err := ini.Load("./secrets.ini")
	if err != nil {
		log.Fatalf("Failed to read file: %v", err)
	}
	dbHost := cfg.Section("database").Key("DB_HOST").String()
	dbPort := cfg.Section("database").Key("DB_PORT").MustInt()
	dbName := cfg.Section("database").Key("DB_NAME").String()
	dbUser := cfg.Section("database").Key("DB_USER").String()
	dbPassword := cfg.Section("database").Key("DB_PASSWORD").String()
	secretKey := cfg.Section("secret").Key("SECRET_KEY").String()

	log.Println("Database Host:", dbHost)
	log.Println("Database Port:", dbPort)
	log.Println("Database Name:", dbName)
	log.Println("Database User:", dbUser)
	log.Println("Database Password:", dbPassword)
	log.Println("Secret Key:", secretKey)

	stashesRouter := http.NewServeMux()
	stashesRouter.HandleFunc("/test", func(writer http.ResponseWriter, request *http.Request) {
		writer.Write([]byte(`{"message": "OK"}`))
	})

	router := http.NewServeMux()
	// Attach the stashesRouter as a subrouter
	router.Handle("/stashes/", http.StripPrefix("/stashes", stashesRouter))
	router.Handle(
		"/banking/",
		middleware.AuthMiddleware(http.StripPrefix("/banking", endpoints.BankRouter())),
	)
	router.Handle("/auth/", http.StripPrefix("/auth", endpoints.AuthRouter()))

	db := database.GetConnStr(dbHost, dbPort, dbName, dbUser, dbPassword)
	apiRouter := middleware.DbMiddleware(
		middleware.Logging(middleware.ResponseWrapperMiddleware(router)),
		db,
	)
	topRouter := http.NewServeMux()

	topRouter.Handle("/", apiRouter)
	fs := http.FileServer(http.Dir("./docs"))
	topRouter.Handle("/docs/", http.StripPrefix("/docs/", fs))
	topRouter.Handle("/swagger/", httpSwagger.Handler(httpSwagger.URL("/docs/swagger.json")))
	utils.InitSecret(secretKey)
	server := http.Server{
		Addr:    ":80",
		Handler: topRouter,
	}
	log.Println("Server listening on :80")
	_ = server.ListenAndServe()
	defer func(db *sql.DB) {
		_ = db.Close()
	}(db)
}
