package endpoints

import (
	"brigadaServer/crud"
	"brigadaServer/models"
	"database/sql"
	_ "database/sql"
	"encoding/json"
	"errors"
	"net/http"
	"strconv"
)

func BankRouter() *http.ServeMux {
	router := http.NewServeMux()
	router.HandleFunc("GET /bank/{id}/{playerId}", getBankJson)
	router.HandleFunc("GET /banks", getAllBanksJson)
	router.HandleFunc("POST /banks", createBankJson)
	router.HandleFunc("GET /deposit/{id}/{playerId}", getPlayerDeposit)
	// Use POST for compatibility with dayz
	router.HandleFunc("POST /deposit/{id}/{playerId}", updatePlayerDeposit)
	return router
}

// @Tags bank
// @Summary Get all banks
// @Description Get all banks
// @ID get-all-banks
// @Produce json
// @Success 200 {object} models.WrappedResult[[]models.BankSpawn]
// @Failure 500 {object} models.WrappedResult[string]
// @Router /banks [get]
func getAllBanksJson(w http.ResponseWriter, r *http.Request) {
	db := r.Context().Value("db").(*sql.DB)
	banks, err := crud.GetAllBanks(db)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		res := models.WrappedResult[string]{
			Data:   err.Error(),
			Status: -1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	} else {
		res := models.WrappedResult[[]models.BankSpawn]{
			Data:   banks,
			Status: 0,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	}
}

// @Tags bank
// @Summary Get bank by id
// @Description Get bank by id
// @ID get-bank
// @Produce json
// @Param id path int true "Bank ID"
// @Param playerId path string true "Player ID"
// @Success 200 {object} models.WrappedResult[models.Bank]
// @Failure 500 {object} models.WrappedResult[string]
// @Router /bank/{id}/{playerId} [get]
func getBankJson(w http.ResponseWriter, r *http.Request) {
	db := r.Context().Value("db").(*sql.DB)
	id, _ := strconv.Atoi(r.PathValue("id"))
	playerId := r.PathValue("playerId")
	bank, err := crud.GetBank(db, id, playerId)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		res := models.WrappedResult[string]{
			Data:   err.Error(),
			Status: -1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)

	} else {
		res := models.WrappedResult[models.Bank]{
			Data:   *bank,
			Status: 0,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	}
}

// @Tags bank
// @Summary Create bank
// @Description Create bank
// @ID create-bank
// @Accept json
// @Produce json
// @Param bank body models.BankSpawn true "Bank"
// @Success 200 {object} models.WrappedResult[string]
// @Failure 500 {object} models.WrappedResult[string]
// @Router /banks [post]
func createBankJson(w http.ResponseWriter, r *http.Request) {
	db := r.Context().Value("db").(*sql.DB)
	var bank models.BankSpawn
	_ = json.NewDecoder(r.Body).Decode(&bank)
	err := crud.CreateBank(db, &bank)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		res := models.WrappedResult[string]{
			Data:   err.Error(),
			Status: -1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	} else {
		res := models.WrappedResult[string]{
			Data:   "Bank created",
			Status: 0,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	}
}

// @Tags bank
// @Summary Get player deposit
// @Description Get player deposit
// @ID get-player-deposit
// @Produce json
// @Param id path int true "Bank ID"
// @Param playerId path string true "Player ID"
// @Success 200 {object} models.WrappedResult[models.Deposit]
// @Failure 500 {object} models.WrappedResult[string]
// @Router /deposit/{id}/{playerId} [get]
func getPlayerDeposit(w http.ResponseWriter, r *http.Request) {
	db := r.Context().Value("db").(*sql.DB)
	id, _ := strconv.Atoi(r.PathValue("id"))
	playerId := r.PathValue("playerId")
	var deposit *models.Deposit
	var err error
	deposit, err = crud.GetDeposit(db, id, playerId)
	if errors.Is(err, sql.ErrNoRows) {
		deposit = &models.Deposit{
			Amount: 0,
		}
		err = crud.CreateDeposit(
			db,
			id,
			playerId,
			deposit,
		)
	}
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		res := models.WrappedResult[string]{
			Data:   err.Error(),
			Status: -1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)

	} else {
		deposit.Operation = "get"
		res := models.WrappedResult[models.Deposit]{
			Data:   *deposit,
			Status: 0,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	}
}

// @Tags bank
// @Summary Update player deposit
// @Description Update player deposit
// @ID update-player-deposit
// @Accept json
// @Produce json
// @Param id path int true "Bank ID"
// @Param playerId path string true "Player ID"
// @Param deposit body models.Deposit true "Deposit"
// @Success 200 {object} models.WrappedResult[models.Deposit]
// @Failure 500 {object} models.WrappedResult[string]
// @Router /deposit/{id}/{playerId} [put]
func updatePlayerDeposit(w http.ResponseWriter, r *http.Request) {
	db := r.Context().Value("db").(*sql.DB)
	id, _ := strconv.Atoi(r.PathValue("id"))
	playerId := r.PathValue("playerId")
	var deposit models.Deposit
	_ = json.NewDecoder(r.Body).Decode(&deposit)

	bank, errBank := crud.GetBank(db, id, playerId)
	if errBank != nil {
		w.WriteHeader(http.StatusInternalServerError)
		res := models.WrappedResult[string]{
			Data:   errBank.Error(),
			Status: -1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
		return
	}
	currentDeposit, errDep := crud.GetDeposit(db, id, playerId)
	if errDep != nil {
		w.WriteHeader(http.StatusInternalServerError)
		res := models.WrappedResult[string]{
			Data:   errDep.Error(),
			Status: -1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
		return
	}

	if deposit.Operation == "deposit" {
		deposit.Amount = currentDeposit.Amount + deposit.Amount - deposit.Amount*bank.Commission/100
	} else if deposit.Operation == "withdraw" {
		deposit.Amount = currentDeposit.Amount - deposit.Amount - deposit.Amount*bank.Commission/100
	} else {
		deposit.Amount = currentDeposit.Amount
	}
	if deposit.Amount > bank.MaxMoney {
		res := models.WrappedResult[string]{
			Data:   "Deposit amount is more than bank max money",
			Status: 1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
		return
	} else if deposit.Amount < 0 {
		res := models.WrappedResult[string]{
			Data:   "Negative deposit amount is not allowed",
			Status: 1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
		return
	}

	err := crud.UpdateDeposit(db, id, playerId, &deposit)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		res := models.WrappedResult[string]{
			Data:   err.Error(),
			Status: -1,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	} else {
		res := models.WrappedResult[models.Deposit]{
			Data:   deposit,
			Status: 0,
		}
		responseStr, _ := json.Marshal(res)
		_, _ = w.Write(responseStr)
	}

}
