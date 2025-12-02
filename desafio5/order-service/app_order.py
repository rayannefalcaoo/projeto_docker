from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/orders')
def get_orders():
    return jsonify({"service": "Order Service (MS2)", "data": [{"id": 101, "item": "Teclado"}, {"id": 102, "item": "Mouse"}]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)