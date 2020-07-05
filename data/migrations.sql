CREATE TABLE "compras" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"date"	TEXT,
	"time"	TEXT,
	"from_currency"	INTEGER,
	"from_quantity"	REAL,
	"to_currency"	INTEGER,
	"to_quantity"	REAL,
	"P_U"	REAL
)