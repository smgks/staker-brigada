package models

type User struct {
	ID             int    `db:"id"`
	Username       string `db:"username"`
	HashedPassword string `db:"hashed_password"`
}
