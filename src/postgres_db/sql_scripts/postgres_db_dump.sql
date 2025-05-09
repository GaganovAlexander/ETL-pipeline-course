CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    patronimic VARCHAR(64),
    email VARCHAR(256) UNIQUE  NOT NULL,
    phone_number VARCHAR(20) UNIQUE  NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    role_id INT REFERENCES roles(id) ON DELETE SET NULL,
    CONSTRAINT email_format CHECK (email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    CONSTRAINT phone_format CHECK (phone_number ~ '^(\+7|8)\d{10}$')
);
CREATE TABLE IF NOT EXISTS admin_privileges (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    can_see_users_full_data BOOLEAN DEFAULT FALSE,
    can_change_users BOOLEAN DEFAULT FALSE,
    can_delete_users BOOLEAN DEFAULT FALSE,
    can_see_orders BOOLEAN DEFAULT FALSE,
    can_change_orders BOOLEAN DEFAULT FALSE,
    can_manage_products BOOLEAN DEFAULT FALSE,
    can_manage_categories BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    parent_category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    description VARCHAR(1024),
    price NUMERIC,
    category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    stock_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS pick_up_points (
    id BIGSERIAL PRIMARY KEY,
    address_text TEXT NOT NULL,
    location GEOGRAPHY(Point, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS order_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128),
    description TEXT
);
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    status_id INT REFERENCES order_statuses(id) ON DELETE SET NULL,
    shipping_adress_id BIGINT REFERENCES pick_up_points(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS order_items (
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id) ON DELETE SET NULL,
    seller_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    quantity INT,
    price_at_time_of_order NUMERIC,
    CONSTRAINT order_items_pk PRIMARY KEY (order_id, product_id, seller_id),
    CONSTRAINT quantity_positivity_check CHECK (quantity > 0),
    CONSTRAINT price_at_time_of_order_positivity_check CHECK (price_at_time_of_order > 0)
);


CREATE TABLE IF NOT EXISTS payments_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128),
    description TEXT
);
CREATE TABLE IF NOT EXISTS payments_methods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128),
    description TEXT
);
CREATE TABLE IF NOT EXISTS payments (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    status_id INT REFERENCES payments_statuses(id) ON DELETE SET NULL,
    method_id INT REFERENCES payments_methods(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS reviews (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    rating INT NOT NULL,
    comment VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS review_attachments (
    review_id BIGINT REFERENCES reviews(id) ON DELETE CASCADE,
    file_url VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INT NOT NULL,
    CONSTRAINT review_attachments_pk PRIMARY KEY (review_id, file_url)
);

CREATE TABLE IF NOT EXISTS change_logs (
id BIGSERIAL PRIMARY KEY,
entity_name VARCHAR(64) NOT NULL,
entity_id BIGINT NOT NULL,
field_name VARCHAR(128) NOT NULL,
old_value TEXT,
new_value TEXT,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
updated_by_id BIGINT NOT NULL,
change_type VARCHAR(128)
);