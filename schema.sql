CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    username TEXT,
    current_stage TEXT DEFAULT 'scan_1',
    stress INT DEFAULT 0,
    rationality INT DEFAULT 0,
    loyalty INT DEFAULT 0,
    risk INT DEFAULT 0,
    sacrifice INT DEFAULT 0,
    resistance INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
