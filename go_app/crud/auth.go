package crud

import (
	"brigadaServer/models"
	"database/sql"
)

func GetUserByPass(db *sql.DB, login string, hashedPassword string) (*models.User, error) {
	row := db.QueryRow(`
		select id, username, hashed_password
		from auth.users
		where hashed_password = $1 and username = $2
	`, hashedPassword, login)
	var user models.User
	err := row.Scan(&user.ID, user.Username, user.HashedPassword)
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func GetUserByName(db *sql.DB, login string) (*models.User, error) {
	row := db.QueryRow(`
		select id, username, hashed_password
		from auth.users
		where username = $1
	`, login)
	var user models.User
	err := row.Scan(
		&user.ID,
		&user.Username,
		&user.HashedPassword,
	)
	if err != nil {
		return nil, err
	}
	return &user, nil
}
