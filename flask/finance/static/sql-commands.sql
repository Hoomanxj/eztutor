
-- create a table for logs
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    trans_type TEXT NOT NULL CHECK (trans_type IN ('BUY', 'SELL')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


-- create a table for portfolios
CREATE TABLE portfolio (
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL CHECK (shares >= 0),
    PRIMARY KEY (user_id, symbol),
    FOREIGN KEY (user_id) REFERENCES users(id)
);


-- in case there is a need for changing table schema
INSERT INTO log (user_id, symbol, amount, trans_type, timestamp)
SELECT user_id, symbol, amount, trans_type, timestamp
FROM logs;


-- Non-UNIQUE index for efficient searching by symbol
CREATE INDEX idx_portfolio_symbol ON portfolio(symbol);


-- reset logs table (for test)
DELETE FROM logs;
DELETE FROM portfolio;
VACUUM;
