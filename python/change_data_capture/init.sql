-- Create a dedicated replication user
-- This user needs the REPLICATION privilege to read the WAL stream.
CREATE USER rep_user WITH REPLICATION ENCRYPTED PASSWORD 'rep_password';


CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- Set REPLICA IDENTITY to FULL
-- This is crucial for Change Data Capture (CDC). It ensures that, for UPDATE 
-- and DELETE operations, the full old row image is written to the WAL.
-- This is equivalent to MySQL's ROW binlog format.
ALTER TABLE products REPLICA IDENTITY FULL;


-- Create a logical replication slot
-- We use the built-in 'pgoutput' plugin as it avoids the compilation issues 
-- faced with 'wal2json' in minimal (Alpine) containers. 
-- Most CDC tools (like Debezium) can consume pgoutput.
SELECT pg_create_logical_replication_slot('my_replication_slot', 'pgoutput');


-- Grant privileges (Optional, but recommended for clean setup)
-- Grant SELECT permission on the table to the replication user.
GRANT SELECT ON products TO rep_user;


-- Insert initial data (Optional)
INSERT INTO products (name, price) VALUES ('Laptop', 1200.00);
INSERT INTO products (name, price) VALUES ('Mouse', 25.50);

-- Note: No explicit PUBLICATION is created here. 
-- When consuming the stream via pg_recvlogical, the option 
-- '--option="publication_names=ALL"' is typically used to read all table changes.
