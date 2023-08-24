CREATE TABLE Builds (
    build_id SERIAL PRIMARY KEY,
    setup_id INT REFERENCES Setups(setup_id),
    build_number INT,
    status VARCHAR(50),
    url VARCHAR(255),
    start_time TIMESTAMP,
    duration REAL
);

CREATE TABLE Tests (
    test_id SERIAL PRIMARY KEY,
    build_id INT REFERENCES Builds(build_id),
    name VARCHAR(255),
    status VARCHAR(50),
    error_message TEXT
);

CREATE TABLE Setups (
    setup_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT
);
