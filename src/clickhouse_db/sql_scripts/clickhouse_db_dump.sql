CREATE TABLE products (
    name String,
    description String,
    price Float64,
    category_name String,
    stock_quantity UInt64,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY created_at;

CREATE TABLE orders (
    user_name String,
    user_role String,
    status_id UInt32,
    address_text String,
    location Array(Float64),
    product_name String,
    seller_name String,
    quantity UInt32,
    price_at_time_of_order Float64,
    created_at DateTime
) ENGINE = MergeTree()
PARTITION BY status_id
ORDER BY created_at;

CREATE TABLE payments (
    order_status String,
    order_cost Float,
    order_items_cout UInt64,
    status_id UInt64,
    method_id UInt64,
    created_at DateTime
) ENGINE = MergeTree()
PARTITION BY tuple(status_id, method_id)
ORDER BY created_at;

CREATE TABLE reviews (
    user_id UInt64,
    product_id UInt64,
    rating Int32,
    comment String,
    attachments_count UInt32,
    has_photo Bool,
    has_video Bool,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY created_at;


CREATE TABLE change_logs (
    entity_name String,
    field_name String,
    updated_at DateTime,
    updated_by_id UInt64,
    change_type String
) ENGINE = MergeTree()
ORDER BY updated_at;
