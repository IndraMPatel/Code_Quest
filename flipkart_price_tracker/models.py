import sqlite3

def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        reviews TEXT,
        total_purchases TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        price TEXT,
        date TEXT,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')
    conn.commit()
    conn.close()

def add_product(title, description, reviews, total_purchases):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (title, description, reviews, total_purchases) VALUES (?, ?, ?, ?)',
                   (title, description, reviews, total_purchases))
    conn.commit()
    conn.close()

def add_price(product_id, price, date):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO price_history (product_id, price, date) VALUES (?, ?, ?)',
                   (product_id, price, date))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def get_price_history(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM price_history WHERE product_id=?', (product_id,))
    history = cursor.fetchall()
    conn.close()
    return history
