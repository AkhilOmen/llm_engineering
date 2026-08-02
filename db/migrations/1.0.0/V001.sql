CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS core_schema;

CREATE TABLE IF NOT EXISTS core_schema.pricing (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    departure_city     VARCHAR(100) NOT NULL,
    destination_city   VARCHAR(100) NOT NULL,
    price               NUMERIC(10,2) NOT NULL,
    currency            VARCHAR(10) NOT NULL,
    effective_date      DATE NOT NULL,
    created_at          TIMESTAMP NOT NULL,
    updated_at          TIMESTAMP NOT NULL
);

INSERT INTO core_schema.pricing (
    departure_city, destination_city, price, currency, effective_date, created_at,updated_at
)
VALUES
('Hyderabad', 'Benglore', 2500.00, 'INR', CURRENT_DATE, NOW(), NOW()),
('Hyderabad', 'Goa', 1800.00, 'INR', CURRENT_DATE, NOW(), NOW()),
('Hyderabad', 'Srinagar', 3200.00, 'INR', CURRENT_DATE, NOW(), NOW());

