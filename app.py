from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# Veritabanı dosya yolu (Konteyner içinde /data klasöründe tutacağız)
DB_PATH = '/data/coffee_shop.db'

def init_db():
    # /data klasörü yoksa oluştur (Hata almamak için)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            customer TEXT NOT NULL,
            status TEXT DEFAULT 'Hazırlanıyor ⏳'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "☕ Kalıcı DevOps Coffee Shop v3.0 - Veriler Artık Güvende!"

@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data or 'item' not in data:
        return jsonify({"error": "Eksik bilgi!"}), 400
    
    item = data['item']
    customer = data.get('customer', 'Anonim')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (item, customer) VALUES (?, ?)', (item, customer))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Siparişiniz ({item}) veritabanına kaydedildi!"}), 201

@app.route('/orders')
def list_orders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    rows = cursor.fetchall()
    conn.close()
    
    orders = [{"id": r[0], "item": r[1], "customer": r[2], "status": r[3]} for r in rows]
    return jsonify({"database_orders": orders})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)