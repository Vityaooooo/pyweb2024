CREATE TABLE IF NOT EXISTS table_counter (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    client_info TEXT NOT NULL
);