package database

import (
	"database/sql"
	_ "github.com/lib/pq"
	"log"
	"strconv"
)

func GetConnStr(
	dbHost string,
	dbPort int,
	dbName string,
	dbUser string,
	dbPassword string,
) *sql.DB {
	connectString := "host=" + dbHost +
		" port=" + strconv.Itoa(dbPort) +
		" user=" + dbUser +
		" password=" + dbPassword +
		" dbname=" + dbName +
		" sslmode=disable"

	db, err := sql.Open("postgres", connectString)
	if err != nil {
		log.Fatal(err)
	}
	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}
	return db
}
