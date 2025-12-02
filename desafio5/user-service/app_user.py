from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/users')
def get_users():
    return jsonify({"service": "User Service (MS1)", "data": [{"id": 1, "name": "Maria"}, {"id": 2, "name": "João"}]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)