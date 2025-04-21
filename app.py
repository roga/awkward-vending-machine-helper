# app.py

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="/var/www/food.roga.tw/.env") # load .env

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from payment_manager import PaymentManager

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/balance', methods=['GET'])
def check_balance():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Missing code'}), 400
    pm = PaymentManager(code)
    result = pm.get_balance()
    return jsonify({'code': code, 'balance': result})

@app.route('/price', methods=['GET'])
def check_price():
    vid = request.args.get('vid')
    if not vid:
        return jsonify({'error': 'Missing vending machine ID'}), 400
    pm = PaymentManager('dummy')  # 不需要個人代碼也可查價格
    result = pm.get_current_product_price(vid)
    return jsonify({'vid': vid, 'price': result})

@app.route('/pay', methods=['POST'])
def pay_product():
    code = request.form.get('code')
    vid = request.form.get('vid')
    price = request.form.get('price')

    if not all([code, vid, price]):
        return jsonify({'error': 'Missing code, vid, or price'}), 400

    pm = PaymentManager(code)
    result = pm.pay(price, vid)
    return jsonify({'code': code, 'vid': vid, 'price': price, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
