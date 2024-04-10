package crud

import (
	"brigadaServer/models"
	"database/sql"
)

func GetAllBanks(db *sql.DB) ([]models.BankSpawn, error) {
	rows, err := db.Query(`
		select bank.id, default_commission, default_max_money, x, y, z, x_dir, y_dir, z_dir 
		from brigada.bank 
		    join brigada.position on bank.position_id = position.id
	`)
	if err != nil {
		return nil, err
	}
	defer func(rows *sql.Rows) {
		_ = rows.Close()
	}(rows)
	var banks []models.BankSpawn
	for rows.Next() {
		var bank models.Bank
		var position models.Position
		err := rows.Scan(&bank.ID, &bank.Commission, &bank.MaxMoney, &position.X, &position.Y, &position.Z, &position.XDir, &position.YDir, &position.ZDir)
		if err != nil {
			return nil, err
		}
		banks = append(
			banks,
			models.BankSpawn{
				Bank:     bank,
				Position: position,
			},
		)
	}
	return banks, nil
}

func GetBank(db *sql.DB, id int, playerId string) (*models.Bank, error) {
	row := db.QueryRow(`
	select bank.id, default_commission, default_max_money, max_money, commission
		from brigada.bank
			join brigada.player on player.steam_id = $2
			left join brigada.player_bank_property on bank.id = player_bank_property.bank_id
			 and player_bank_property.player_id = player.id
		where bank.id = $1
	`, id, playerId)
	var bank *models.Bank
	var defaultCommission sql.NullInt64
	var defaultMaxMoney sql.NullInt64
	var maxMoney sql.NullInt64
	var commission sql.NullInt64
	var bankId int
	err := row.Scan(&bankId, &defaultCommission, &defaultMaxMoney, &maxMoney, &commission)
	if err != nil {
		return nil, err
	}
	bank = &models.Bank{
		ID: bankId,
	}
	if commission.Valid {
		bank.Commission = int(commission.Int64)
	} else {
		bank.Commission = int(defaultCommission.Int64)
	}
	if maxMoney.Valid {
		bank.MaxMoney = int(maxMoney.Int64)
	} else {
		bank.MaxMoney = int(defaultMaxMoney.Int64)
	}
	return bank, nil
}

func CreateBank(db *sql.DB, bank *models.BankSpawn) error {
	positionId := 0
	errPos := db.QueryRow(`
		insert into brigada.position (x, y, z, x_dir, y_dir, z_dir)
		values ($1, $2, $3, $4, $5, $6)
		returning id
	`, bank.Position.X, bank.Position.Y, bank.Position.Z, bank.Position.XDir, bank.Position.YDir, bank.Position.ZDir).Scan(&positionId)
	if errPos != nil {
		return errPos
	}
	_, err := db.Exec(`
		insert into brigada.bank (default_commission, default_max_money, position_id)
		values ($1, $2 , $3)
	`, bank.Bank.Commission, bank.Bank.MaxMoney, positionId)
	return err
}

func UpdateBank(db *sql.DB, bank *models.Bank) error {
	_, err := db.Exec(`
		update brigada.bank
		set default_commission = $2, default_max_money = $3
		where id = $1
	`, bank.ID, bank.Commission, bank.MaxMoney)
	return err
}

func GetDeposit(db *sql.DB, bankId int, playerId string) (*models.Deposit, error) {
	row := db.QueryRow(`
		select money from brigada.deposit
			 join brigada.player on player.steam_id = $1
			 where bank_id = $2 and player_id = player.id;
	`, playerId, bankId)
	deposit := new(models.Deposit)
	err := row.Scan(&deposit.Amount)
	if err != nil {
		return nil, err
	}
	return deposit, nil
}

func CreateDeposit(db *sql.DB, bankId int, playerId string, deposit *models.Deposit) error {
	_, err := db.Exec(`
		insert into brigada.deposit (player_id, money, bank_id)
		values ((select id from brigada.player where steam_id = $1), $2, $3)
	`, playerId, deposit.Amount, bankId)
	return err
}

func UpdateDeposit(db *sql.DB, bankId int, playerId string, deposit *models.Deposit) error {
	_, err := db.Exec(`
		update brigada.deposit
		set money = $2
		where player_id = (select id from brigada.player where steam_id = $1)
		and bank_id = $3
	`, playerId, deposit.Amount, bankId)
	return err
}
