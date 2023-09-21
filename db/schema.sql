-- Setups Table
CREATE TABLE Setups (
    setup_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    comment TEXT
);

-- Scopes Table
CREATE TABLE Scopes (
    scope_id SERIAL PRIMARY KEY,
    setup_id INT REFERENCES Setups(setup_id),
    name VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    completed_tests INT,
    total_tests INT,
    status VARCHAR(50)
);

-- Tests Table
CREATE TABLE Tests (
    test_id SERIAL PRIMARY KEY,
    scope_id INT REFERENCES Scopes(scope_id),
    name VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50)
);

-- JenkinsInfo Table
CREATE TABLE JenkinsInfo (
    jenkins_info_id SERIAL PRIMARY KEY,
    setup_id INT REFERENCES Setups(setup_id),
    last_runs TEXT -- or JSON depending on your needs
);

-- FailingTestCases Table
CREATE TABLE FailingTestCases (
    failing_tc_id SERIAL PRIMARY KEY,
    setup_id INT REFERENCES Setups(setup_id),
    test_id INT REFERENCES Tests(test_id),
    failing_test_cases TEXT -- or JSON depending on your needs
);
