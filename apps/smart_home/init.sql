CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    temperature FLOAT
);

INSERT INTO sensors (name, location, temperature) VALUES 
('Living Room Sensor', 'Living Room', 22.5);
