package endpoints

import (
	"brigadaServer/crud"
	"brigadaServer/models"
	"brigadaServer/utils"
	"database/sql"
	"encoding/json"
	"net/http"
)

func AuthRouter() *http.ServeMux {
	router := http.NewServeMux()
	router.HandleFunc("POST /token_json", tokenJson)
	return router
}

// @Tags auth
// @Summary Get token
// @Description Get token
// @ID get-token
// @Accept json
// @Produce json
// @Param request body models.UserSignIn true "User sign in"
// @Success 200 {object} models.TokenResponse
// @Failure 401 {object} models.WrappedResult[string]
// @Router /token_json [post]
func tokenJson(w http.ResponseWriter, r *http.Request) {
	var userSignInRequest models.UserSignIn
	_ = json.NewDecoder(r.Body).Decode(&userSignInRequest)
	db := r.Context().Value("db").(*sql.DB)
	user, _ := crud.GetUserByName(db, userSignInRequest.Login)
	if user == nil {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
	if utils.ValidatePassword(userSignInRequest.Password, user.HashedPassword) {
		token, _ := utils.GenerateToken(uint(user.ID))
		response := models.TokenResponse{
			AccessToken: token,
			TokenType:   "Bearer",
		}
		responseStr, _ := json.Marshal(response)
		_, _ = w.Write(responseStr)
	} else {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}
}
