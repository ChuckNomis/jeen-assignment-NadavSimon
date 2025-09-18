
-- Simple Users Table Schema
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    balance NUMERIC(10, 2) DEFAULT 0.00,
    active BOOLEAN DEFAULT TRUE
);
