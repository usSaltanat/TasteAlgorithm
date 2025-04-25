DROP DATABASE if EXISTS taste_algorithm;

CREATE DATABASE taste_algorithm;

CREATE TABLE IF NOT exists units (
    id SERIAL PRIMARY KEY,
    unit VARCHAR NOT null,
    UNIQUE (unit)
);

CREATE TABLE IF NOT exists categories  (
    id SERIAL PRIMARY KEY,
    category VARCHAR NOT NULL,
    UNIQUE (category)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    unit_id INT NOT NULL,
    category_id INT NULL,
    product_name VARCHAR NOT NULL,
    UNIQUE (product_name, unit_id, category_id),
    CONSTRAINT fk_unit FOREIGN KEY(unit_id) REFERENCES units(id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_category FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS meals_categories (
    id SERIAL PRIMARY KEY,
    meals_category VARCHAR NOT NULL,
    UNIQUE (meals_category)
);

CREATE TABLE IF NOT EXISTS meals (
    id SERIAL PRIMARY KEY,
    meal VARCHAR NOT NULL,
    meal_category_id INT NULL,
    UNIQUE (meal, meal_category_id),
    CONSTRAINT fk_category_meal FOREIGN KEY(meal_category_id) REFERENCES meals_categories(id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS meals_compositions (
    id SERIAL PRIMARY KEY,
    meal_id INT NULL,
    product_id INT NULL,
    per_portion FLOAT NULL,
    portions INT NULL,
    portions_size FLOAT NULL,
    CONSTRAINT fk_meal FOREIGN KEY(meal_id) REFERENCES meals(id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_product FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    meal_id INT NULL,
    body_meal_recipes VARCHAR NULL,
    CONSTRAINT fk_meal FOREIGN KEY(meal_id) REFERENCES meals(id) ON DELETE RESTRICT ON UPDATE RESTRICT
);


