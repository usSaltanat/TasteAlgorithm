DROP DATABASE if EXISTS taste_algorithm;

CREATE DATABASE taste_algorithm;


CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login VARCHAR NOT NULL,
    password_hash VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_session (
    user_id INT NOT NULL,
    session_uuid VARCHAR NOT NULL,
    -- created_at TIMESTAMP NOT NULL,
    UNIQUE (session_uuid),
    CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT exists units (
    id SERIAL PRIMARY KEY,
    unit VARCHAR NOT null,
    user_id INT NOT NULL,
    UNIQUE (user_id, unit),
    CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT exists categories  (
    id SERIAL PRIMARY KEY,
    category VARCHAR NOT NULL,
    user_id INT NOT NULL,
    UNIQUE (user_id, category),
    CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    unit_id INT NOT NULL,
    category_id INT NULL,
    product_name VARCHAR NOT NULL,
    user_id INT NOT NULL,
    UNIQUE (user_id, product_name, unit_id, category_id),
    CONSTRAINT fk_unit FOREIGN KEY(unit_id) REFERENCES units(id) ON DELETE CASCADE ON UPDATE RESTRICT,
    CONSTRAINT fk_category FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE ON UPDATE RESTRICT,
    CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
);

--drop table meals_categories
CREATE TABLE IF NOT EXISTS meals_categories (
    id INT NOT NULL,
    meals_category VARCHAR NOT NULL,
    user_id INT NOT NULL,
    UNIQUE (id, user_id, meals_category),
    CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS meals (
    id SERIAL PRIMARY KEY,
    meal VARCHAR NOT NULL,
    meal_category_id INT NULL,
    user_id INT NOT NULL,
    description TEXT NULL,
    UNIQUE (user_id, meal, meal_category_id),
--    CONSTRAINT fk_category_meal FOREIGN KEY(meal_category_id, user_id) REFERENCES meals_categories(id, user_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
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
