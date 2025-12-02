from flask import Flask, jsonify
app = Flask(__name__)

USUARIOS = [
    {"id": 1, "nome": "Alice", "ativo_desde": "2023-01-15"},
    {"id": 2, "nome": "Bob", "ativo_desde": "2023-03-20"},
    {"id": 3, "nome": "Carol", "ativo_desde": "2023-05-10"}
]

@app.route('/users')
def list_users():
    return jsonify(USUARIOS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)