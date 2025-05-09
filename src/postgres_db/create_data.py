from mimesis import Generic

from src.postgres_db import conn, cur

generic = Generic('ru')

def table_has_data(table_name):
    cur.execute(f"SELECT EXISTS (SELECT 1 FROM {table_name} LIMIT 1);")
    return cur.fetchone()[0]

def roles():
    if table_has_data('roles'):
        return
    cur.execute("""
        --sql
        INSERT INTO roles(name) VALUES 
            ('user'),
            ('admin'),
            ('seller');
    """)
    conn.commit()

def users():
    if table_has_data('users'):
        return
    cur.execute('SELECT id FROM roles;')
    role_ids = cur.fetchall()
    users_roles = list(role_ids[0] * 20_000 + role_ids[1] * 50 + role_ids[2] * 500)
    generic.random.shuffle(users_roles)
    for role in users_roles:
        cur.execute("""
            --sql
            INSERT INTO users(password_hash, first_name, last_name, email, phone_number, created_at, role_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, ('',
              generic.person.first_name(),
              generic.person.last_name(),
              generic.person.email(unique=True),
              generic.person.phone_number('+7##########'),
              generic.datetime.datetime(),
              role))
    conn.commit()

def categories():
    if table_has_data('categories'):
        return
    for _ in range(10):
        cur.execute("INSERT INTO categories(name) VALUES(%s);", (generic.text.word(),))
    for _ in range(200):
        cur.execute("INSERT INTO categories(name, parent_category_id) VALUES(%s, %s);",
                    (generic.text.word(), generic.random.randint(1, 10)))
    conn.commit()

def random_price():
    return round(generic.random.random()*generic.random.randint(100, 100_000), 2)

def products():
    if table_has_data('products'):
        return
    cur.execute('SELECT MIN(id), MAX(id) FROM categories;')
    category_ids = cur.fetchone()
    for _ in range(500):
        cur.execute("""
            --sql
            INSERT INTO products(name, description, price, category_id, stock_quantity, created_at)
            VALUES(%s, %s, %s, %s, %s, %s);
        """, (generic.text.word(),
              None if generic.random.randint(1, 10) == 1 else generic.text.text(2)[:1024],
              random_price(),
              generic.random.randint(*category_ids),
              generic.random.randint(1, 500),
              generic.datetime.datetime()))
    conn.commit()

def pick_up_points():
    if table_has_data('pick_up_points'):
        return
    for _ in range(100):
        cur.execute("""
            --sql
            INSERT INTO pick_up_points(address_text, location, created_at)
            VALUES(%s, ST_GeogFromText('SRID=4326;POINT(%s %s)'), %s);
        """, (generic.address.address(),
              generic.address.latitude(),
              generic.address.longitude(),
              generic.datetime.datetime()))
    conn.commit()

def order_statuses():
    if table_has_data('order_statuses'):
        return
    cur.execute("""
        --sql
        INSERT INTO order_statuses(name) VALUES 
            ('created'), ('paid'), ('packing'), ('packed'), 
            ('transit'), ('arrived'), ('received'), ('canceled');
    """)
    conn.commit()

def orders():
    if table_has_data('orders'):
        return
    cur.execute('SELECT MIN(id), MAX(id) FROM users;')
    user_ids = cur.fetchone()
    cur.execute('SELECT MIN(id), MAX(id) FROM pick_up_points;')
    address_ids = cur.fetchone()
    cur.execute('SELECT MIN(id), MAX(id) FROM order_statuses;')
    status_ids = cur.fetchone()

    cur.execute('SELECT MIN(id), MAX(id) FROM products;')
    product_ids = cur.fetchone()

    for _ in range(100_000):
        cur.execute("""
            --sql
            INSERT INTO orders(user_id, status_id, shipping_adress_id, created_at)
            VALUES(%s, %s, %s, %s)
            RETURNING id;
        """, (generic.random.randint(*user_ids),
              generic.random.randint(*status_ids),
              generic.random.randint(*address_ids),
              generic.datetime.datetime()))
        
        res = cur.fetchone()
        if res is None:
            continue

        cur.execute("""
            --sql
            INSERT INTO order_items(order_id, product_id, seller_id, quantity, price_at_time_of_order)
            VALUES(%s, %s, %s, %s, %s)
            ON CONFLICT (order_id, product_id, seller_id) DO NOTHING;
        """, (res[0],
              generic.random.randint(*product_ids),
              generic.random.randint(user_ids[1] - 500, user_ids[1]),
              generic.random.randint(1, 30),
              random_price()))
    conn.commit()

def order_items():
    if table_has_data('order_items'):
        return
    cur.execute('SELECT MIN(id), MAX(id) FROM orders;')
    order_ids = cur.fetchone()
    cur.execute('SELECT MIN(id), MAX(id) FROM products;')
    product_ids = cur.fetchone()
    cur.execute('SELECT MIN(id), MAX(id) FROM users;')
    user_ids = cur.fetchone()

    for _ in range(200_000):
        cur.execute("""
            --sql
            INSERT INTO order_items(order_id, product_id, seller_id, quantity, price_at_time_of_order)
            VALUES(%s, %s, %s, %s, %s)
            ON CONFLICT (order_id, product_id, seller_id) DO NOTHING;
        """, (generic.random.randint(*order_ids),
              generic.random.randint(*product_ids),
              generic.random.randint(user_ids[1] - 500, user_ids[1]),
              generic.random.randint(1, 30),
              random_price()))
    conn.commit()

def payments_statuses():
    if table_has_data('payments_statuses'):
        return
    cur.execute("""
        --sql
        INSERT INTO payments_statuses(name) VALUES 
            ('created'), ('completed'), ('canceled');
    """)
    conn.commit()

def payments_methods():
    if table_has_data('payments_methods'):
        return
    cur.execute("""
        --sql
        INSERT INTO payments_methods(name) VALUES 
            ('cash'), ('card'), ('online');
    """)
    conn.commit()

def payments():
    if table_has_data('payments'):
        return
    cur.execute('SELECT MIN(id), MAX(id) FROM orders;')
    order_ids = cur.fetchone()
    cur.execute('SELECT MIN(id), MAX(id) FROM payments_statuses;')
    status_ids = cur.fetchone()
    cur.execute('SELECT MIN(id), MAX(id) FROM payments_methods;')
    method_ids = cur.fetchone()

    for order_id in range(order_ids[0], order_ids[1] + 1):
        cur.execute("""
            --sql
            INSERT INTO payments(order_id, status_id, method_id, created_at)
            VALUES(%s, %s, %s, %s);
        """, (order_id,
              generic.random.randint(*status_ids),
              generic.random.randint(*method_ids),
              generic.datetime.datetime()))
    conn.commit()

def reviews():
    if table_has_data('reviews'):
        return
    cur.execute('SELECT MIN(id), MAX(id) FROM users;')
    user_ids = cur.fetchone()
    cur.execute('SELECT MIN(id), MAX(id) FROM products;')
    product_ids = cur.fetchone()

    for _ in range(50_000):
        cur.execute("""
            --sql
            INSERT INTO reviews(user_id, product_id, rating, comment, created_at)
            VALUES(%s, %s, %s, %s, %s);
        """, (generic.random.randint(*user_ids),
              generic.random.randint(*product_ids),
              generic.random.randint(1, 10),
              generic.text.text(2)[:512],
              generic.datetime.datetime()))
    conn.commit()

def review_attachments():
    if table_has_data('review_attachments'):
        return
    cur.execute('SELECT MIN(id), MAX(id) FROM reviews;')
    review_ids = cur.fetchone()
    file_types = ['photo', 'video']
    for _ in range(5_000):
        cur.execute("""
            --sql
            INSERT INTO review_attachments(review_id, file_url, file_type, file_size)
            VALUES(%s, %s, %s, %s);
        """, (generic.random.randint(*review_ids),
              generic.internet.url(),
              generic.random.choice(file_types),
              generic.random.randint(512, 20*1024)))
    conn.commit()

def change_logs():
    if table_has_data('change_logs'):
        return
    cur.execute('SELECT MIN(id), MAX(id) FROM users;')
    user_ids = cur.fetchone()
    tables = ['users', 'categories', 'products', 'pick_up_points', 'orders', 'order_items', 'payments', 'reviews']
    change_types = ['set', 'update', 'delete']
    for _ in range(50_000):
        cur.execute("""
            --sql
            INSERT INTO change_logs(entity_name, entity_id, field_name, old_value, new_value, updated_at, updated_by_id, change_type)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
        """, (generic.random.choice(tables),
              generic.random.randint(1, 10_000),
              generic.random.choice(tables + ['name', 'description']),
              generic.text.word(),
              generic.text.word(),
              generic.datetime.datetime(),
              generic.random.randint(user_ids[1]-550, user_ids[1]-500),
              generic.random.choice(change_types)))
    conn.commit()
