-- Business Listings Intelligence Platform
-- MySQL Database Initialization & Schema Definition
-- Target Database: business_listings_db
-- Target Table: listing_master

CREATE DATABASE IF NOT EXISTS business_listings_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE business_listings_db;

DROP TABLE IF EXISTS listing_master;

CREATE TABLE listing_master (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    address TEXT,
    phone VARCHAR(30),
    source VARCHAR(100) NOT NULL,
    source_id VARCHAR(150),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY unique_source_listing (source, source_id),
    INDEX idx_city (city),
    INDEX idx_category (category),
    INDEX idx_source (source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

