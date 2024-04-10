package models

type UserSignIn struct {
	Login    string `json:"login"`
	Password string `json:"password"`
}

type TokenResponse struct {
	AccessToken string `json:"access_token"`
	TokenType   string `json:"token_type"`
}

type WrappedResult[T any] struct {
	Data   T   `json:"data"`
	Status int `json:"status"`
}

type Deposit struct {
	Amount    int    `json:"amount"`
	Operation string `json:"operation"` // "deposit" or "withdraw" or "get"
}

type Bank struct {
	ID         int `json:"id"`
	Commission int `json:"commission"`
	MaxMoney   int `json:"max_money"`
}

type Position struct {
	X    float64 `json:"x"`
	Y    float64 `json:"y"`
	Z    float64 `json:"z"`
	XDir float64 `json:"x_dir"`
	YDir float64 `json:"y_dir"`
	ZDir float64 `json:"z_dir"`
}

type BankSpawn struct {
	Bank     Bank     `json:"bank"`
	Position Position `json:"position"`
}
