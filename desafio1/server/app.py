from flask import Flask
import os

HOST_ID = os.uname()[1] 

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'Olá, Mundo! Este é o container: {HOST_ID}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)