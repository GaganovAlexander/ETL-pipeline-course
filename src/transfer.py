from src.postgres_db import cur
from src.clickhouse_db import client


def transfer_products():
    cur.execute("""
        --sql
        SELECT p.name, p.description, p.price::float, c.category_name, p.stock_quantity, p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id;
    """)
    data = cur.fetchall()

    client.command("TRUNCATE TABLE products")
    client.insert(
        "products",
        data,
        column_names=["name", "description", "price", "category_name", "stock_quantity", "created_at"]
    )

def transfer_orders():
    cur.execute("""
        --sql
        SELECT 
            CONCAT(u.first_name, ' ', u.last_name) AS user_name, 
            r.name AS user_role,
            o.status_id, 
            p.address_text, 
            ARRAY[ST_X(p.location::geometry), ST_Y(p.location::geometry)] AS location,
            pr.name AS product_name, 
            CONCAT(s.first_name, ' ', s.last_name) AS seller_name, 
            oi.quantity, 
            oi.price_at_time_of_order, 
            o.created_at
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        LEFT JOIN roles r ON u.role_id = r.id
        LEFT JOIN pick_up_points p ON o.shipping_adress_id = p.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN products pr ON oi.product_id = pr.id
        LEFT JOIN users s ON oi.seller_id = s.id;
    """)
    data = cur.fetchall()

    client.command("TRUNCATE TABLE orders")
    client.insert(
        "orders",
        data,
        column_names=["user_name", "user_role", "status_id", "address_text", "location", "product_name", "seller_name", "quantity", "price_at_time_of_order", "created_at"]
    )

def transfer_payments():
    cur.execute("""
        --sql
        SELECT 
            os.name AS order_status, 
            SUM(oi.price_at_time_of_order * oi.quantity) AS order_cost, 
            COUNT(*) AS order_items_count, 
            p.status_id, 
            p.method_id, 
            p.created_at
        FROM payments p
        LEFT JOIN orders o ON p.order_id = o.id
        LEFT JOIN order_statuses os ON o.status_id = os.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        GROUP BY os.name, p.status_id, p.method_id, p.created_at;
    """)
    data = cur.fetchall()

    client.command("TRUNCATE TABLE payments")
    client.insert(
        "payments",
        data,
        column_names=["order_status", "order_cost", "order_items_count", "status_id", "method_id", "created_at"]
    )

def transfer_reviews():
    cur.execute("""
        --sql
        SELECT 
            r.user_id, 
            r.product_id, 
            r.rating, 
            r.comment, 
            COUNT(ra.file_url) AS attachments_count, 
            BOOL_OR(ra.file_type LIKE 'image/%') AS has_photo, 
            BOOL_OR(ra.file_type LIKE 'video/%') AS has_video, 
            r.created_at
        FROM reviews r
        LEFT JOIN review_attachments ra ON r.id = ra.review_id
        GROUP BY r.id;
    """)
    data = cur.fetchall()

    client.command("TRUNCATE TABLE reviews")
    client.insert(
        "reviews",
        data,
        column_names=["user_id", "product_id", "rating", "comment", "attachments_count", "has_photo", "has_video", "created_at"]
    )

def transfer_change_logs():
    cur.execute("""
        --sql
        SELECT 
            entity_name, 
            field_name, 
            updated_at, 
            updated_by_id, 
            change_type
        FROM change_logs;
    """)
    data = cur.fetchall()

    client.command("TRUNCATE TABLE change_logs")
    client.insert(
        "change_logs",
        data,
        column_names=["entity_name", "field_name", "updated_at", "updated_by_id", "change_type"]
    )
