-- create businesses table
CREATE TABLE IF NOT EXISTS businesses (
    business_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(50),
        url VARCHAR(250),
        address VARCHAR(50),
        city VARCHAR(50),
        state VARCHAR(50),
        postal_code INT,
        review_count INT,
        rating FLOAT,
        price VARCHAR(50));

CREATE TABLE IF NOT EXISTS categories(
        category_id SERIAL PRIMARY KEY,
        alias VARCHAR(50),
        title VARCHAR(50)
    );

CREATE TABLE IF NOT EXISTS business_categories(
        id SERIAL PRIMARY KEY,
        business_id VARCHAR(50),
        category_id INT
    );

CREATE TABLE IF NOT EXISTS is_mobile_friendly(
        business_id VARCHAR PRIMARY KEY,
        mobile_friendliness BOOLEAN,
        screenshot VARCHAR,
        last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS mobile_issues(
        id SERIAL PRIMARY KEY,
        business_id VARCHAR(50),
        mobileFriendlyIssues VARCHAR,
        last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS gmb(
        business_id VARCHAR(50) PRIMARY KEY,
        verified_status BOOLEAN,
        last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS zip_codes(
        id SERIAL PRIMARY KEY,
        zip_code INT,
        city VARCHAR(50),
        county VARCHAR(50),
        type VARCHAR(50)
    );

CREATE TABLE IF NOT EXISTS business_websites(
        business_id VARCHAR(50) PRIMARY KEY,
        business_url VARCHAR(50),
        last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );