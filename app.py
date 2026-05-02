from flask import Flask, jsonify, request

app = Flask(__name__)

# Geçici veri tabanı (Konteyner her restart olduğunda sıfırlanır)
menu = {
    "espresso": {"name": "Espresso", "price": 50},
    "latte": {"name": "Latte", "price": 70},
    "americano": {"name": "Americano", "price": 60}
}
orders = []

@app.route('/')
def home():
    return "☕ DevOps Coffee Shop API v2.0 - /menu ile ürünleri gör, /order ile sipariş ver!"

@app.route('/menu')
def get_menu():
    return jsonify({"status": "available", "items": menu})

@app.route('/order', methods=['POST'])
def place_order():
    # Kullanıcıdan JSON verisi bekliyoruz: {"item": "latte", "customer": "Batus"}
    data = request.get_json()
    
    if not data or 'item' not in data:
        return jsonify({"error": "Eksik bilgi! 'item' belirtmelisiniz."}), 400
    
    item_key = data['item'].lower()
    if item_key not in menu:
        return jsonify({"error": "Bu ürün menümüzde yok!"}), 404
    
    new_order = {
        "order_id": len(orders) + 1,
        "item": menu[item_key]['name'],
        "customer": data.get('customer', 'Anonim'),
        "status": "Hazırlanıyor ⏳"
    }
    orders.append(new_order)
    return jsonify({"message": "Sipariş alındı!", "details": new_order}), 201

@app.route('/orders')
def list_orders():
    return jsonify({"active_orders": orders})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)