package models

//type User struct {
//	ID       int
//	Username string
//	Password string
//}

//
//type Category struct {
//	ID   int    `db:"id"`
//	Name string `db:"name"`
//}
//
//type Trader struct {
//	ID         int    `db:"id"`
//	Name       string `db:"name"`
//	PositionID int    `db:"position_id"`
//}
//
//type Position struct {
//	ID   int     `db:"id"`
//	X    float64 `db:"x"`
//	Y    float64 `db:"y"`
//	Z    float64 `db:"z"`
//	XDir float64 `db:"x_dir"`
//	YDir float64 `db:"y_dir"`
//	ZDir float64 `db:"z_dir"`
//}
//
//type TraderInventory struct {
//	ID         int    `db:"id"`
//	TraderID   int    `db:"trader_id"`
//	SkinName   string `db:"skin_name"`
//	VestID     *int   `db:"vest_id"`
//	BackpackID *int   `db:"backpack_id"`
//	TopID      *int   `db:"top_id"`
//	BeltID     *int   `db:"belt_id"`
//	LegsID     *int   `db:"legs_id"`
//	HeadID     *int   `db:"head_id"`
//	FaceID     *int   `db:"face_id"`
//	EyesID     *int   `db:"eyes_id"`
//	GlovesID   *int   `db:"gloves_id"`
//	FeetID     *int   `db:"feet_id"`
//	ArmbandID  *int   `db:"armband_id"`
//}
//
//type TraderCategory struct {
//	ID   int    `db:"id"`
//	Name string `db:"name"`
//}
//
//type TraderItems struct {
//	TraderID         int  `db:"trader_id"`
//	ItemID           int  `db:"item_id"`
//	TraderCategoryID int  `db:"traderCategoryID"`
//	Price            *int `db:"price"`
//	SellPrice        *int `db:"sell_price"`
//	Count            *int `db:"count"`
//	Points           *int `db:"points"`
//	RequiredPoints   *int `db:"required_points"`
//}
//
//type Item struct {
//	ID        int    `db:"id"`
//	ClassName string `db:"class_name"`
//}
//
//type Faction struct {
//	ID   int    `db:"id"`
//	Name string `db:"name"`
//}
//
//type Player struct {
//	ID        int    `db:"id"`
//	Name      string `db:"name"`
//	FactionID int    `db:"faction_id"`
//	Level     int    `db:"level"`
//}
//
//type Bank struct {
//	ID         int `db:"id"`
//	Commission int `db:"commission"`
//	MaxMoney   int `db:"max_money"`
//}
//
//type BankDeposit struct {
//	ID       int `db:"id"`
//	PlayerID int `db:"player_id"`
//	Money    int `db:"max_money"`
//	BankID   int `db:"bank_id"`
//}
