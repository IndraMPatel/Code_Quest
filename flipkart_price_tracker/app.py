from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import datetime
import sqlite3

app = Flask(__name__)

# Replace these values with your Flipkart Affiliate details
affiliate_id = 'joel0250g'
affiliate_token = '049f9f9072f148f4acbf86f9c86303fa'

# Database initialization
def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        productId TEXT,
                        title TEXT,
                        description TEXT,
                        price TEXT,
                        reviews TEXT,
                        total_purchases TEXT,
                        url TEXT,
                        timestamp TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS price_history (
                        id INTEGER PRIMARY KEY,
                        product_id INTEGER,
                        price TEXT,
                        date TEXT,
                        FOREIGN KEY (product_id) REFERENCES products(id))''')
    conn.commit()
    conn.close()

# Function to fetch product details from Flipkart API
def fetch_product_details(affiliate_id, affiliate_token, url):
    headers = {
        'Fk-Affiliate-Id': affiliate_id,
        'Fk-Affiliate-Token': affiliate_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Helper to get product info
def extract_product_info(product):
    return {
        'productId': product['productBaseInfoV1']['productId'],
        'title': product['productBaseInfoV1']['title'],
        'price': product['productBaseInfoV1']['flipkartSellingPrice']['amount'],
        'description': product['productBaseInfoV1'].get('productDescription', 'No description available'),
        'reviews': product['productBaseInfoV1']['productReviewCount'],
        'total_purchases': product['productBaseInfoV1'].get('productRating', 'N/A'),
        'url': product['productBaseInfoV1']['productUrl'],
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def index():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/fetch', methods=['POST'])
def fetch():
    product_url = request.form['url']
    category = product_url.split('/')[-1]  # Extract category from URL
    product_response = fetch_product_details(affiliate_id, affiliate_token, product_url)
    
    if product_response and 'productInfoList' in product_response:
        product_info = product_response['productInfoList'][0]
        product = extract_product_info(product_info)
        
        # Insert product into database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (productId, title, description, price, reviews, total_purchases, url, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                        (product['productId'], product['title'], product['description'], product['price'], product['reviews'], product['total_purchases'], product['url'], product['timestamp']))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return jsonify({'status': 'error', 'message': 'Unable to fetch product details'})

@app.route('/recheck/<productId>', methods=['GET'])
def recheck(productId):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE productId=?', (productId,))
    product = cursor.fetchone()

    if product:
        product_url = product[6]
        updated_product = fetch_product_details(affiliate_id, affiliate_token, product_url)
        
        if updated_product:
            # Update price and timestamp
            cursor.execute('UPDATE products SET price=?, timestamp=? WHERE productId=?', 
                           (updated_product['productBaseInfoV1']['flipkartSellingPrice']['amount'], 
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), productId))
            cursor.execute('INSERT INTO price_history (product_id, price, date) VALUES (?, ?, ?)',
                           (product[0], updated_product['productBaseInfoV1']['flipkartSellingPrice']['amount'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
            return jsonify({'status': 'success', 'message': 'Price updated!'})

    return jsonify({'status': 'error', 'message': 'Product not found or unable to recheck price'})

@app.route('/product/<productId>')
def product_detail(productId):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE productId=?', (productId,))
    product = cursor.fetchone()
    
    cursor.execute('SELECT * FROM price_history WHERE product_id=?', (product[0],))
    price_history = cursor.fetchall()
    conn.close()
    
    if product:
        return render_template('product.html', product=product, history=price_history)
    return jsonify({'status': 'error', 'message': 'Product not found'})

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE title LIKE ?', ('%' + query + '%',))
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/filter', methods=['POST'])
def filter():
    min_price = request.form['min_price']
    max_price = request.form['max_price']
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE price BETWEEN ? AND ?', (min_price, max_price))
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
