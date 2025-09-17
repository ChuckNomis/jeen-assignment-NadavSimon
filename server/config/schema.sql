
-- Simple Users Table Schema for Demo Project
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    balance NUMERIC(10, 2) DEFAULT 0.00,
    active BOOLEAN DEFAULT TRUE
);

-- Insert sample data
INSERT INTO users (name, email, balance, active) VALUES
('Alice Johnson', 'alice@example.com', 250.00, TRUE),
('Bob Smith', 'bob@example.com', 100.50, TRUE),
('Charlie Lee', 'charlie@example.com', 0.00, FALSE),
('Diana Prince', 'diana@example.com', 500.75, TRUE),
('Ethan Clark', 'ethan@example.com', 75.25, TRUE);
