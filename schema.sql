DROP DATABASE IF EXISTS stockinformation;
CREATE DATABASE stockinformation;

\c  stockinformation;

CREATE SCHEMA pricing;

SET search_path TO pricing;

CREATE TABLE IF NOT EXISTS company (
    company_id INT GENERATED ALWAYS AS IDENTITY,
    symbol TEXT NOT NULL UNIQUE,
    company_name TEXT NOT NULL,
    PRIMARY KEY (company_id)
);

CREATE TABLE IF NOT EXISTS prices (
    price_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT NOT NULL,
    price_date TIMESTAMP NOT NULL,
    open_price REAL,
    high REAL,
    low REAL,
    close_price REAL,
    adj_close_price REAL,
    volume INT,
    PRIMARY KEY (price_id)
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);