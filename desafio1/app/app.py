from flask import Flask
import datetime

app = Flask(__name__)
PORT = 8080

@app.route("/")
def helloWorld():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resposta = f"Olá, Mundo! \n {timestamp}"

    return resposta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)