DROP DATABASE if EXISTS taste_algorithm;

CREATE DATABASE taste_algorithm;

CREATE TABLE IF NOT exists units (
    id SERIAL PRIMARY KEY,
    unit VARCHAR NOT NULL
);

CREATE TABLE IF NOT exists categories  (
    id SERIAL PRIMARY KEY,
    category VARCHAR NOT NULL,
    UNIQUE (category)
);

CREATE TABLE IF NOT exists products  (
    id SERIAL PRIMARY KEY,
    unit_id INT NOT NULL,
    category_id INT NULL,
    product_name VARCHAR NOT null,

    CONSTRAINT fk_unit FOREIGN KEY(unit_id) REFERENCES units(id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_category FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE RESTRICT
);
