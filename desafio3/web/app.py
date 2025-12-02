from flask import Flask
import redis, os, psycopg2
from time import sleep

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST') 
REDIS_HOST = os.environ.get('REDIS_HOST')

def init_connections():
    global r, conn
    
    print(f"Tentando conectar ao Cache (Redis) em: {REDIS_HOST}")
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    r.set('contador_cache', 0)

    print(f"Tentando conectar ao Banco de Dados em: {DB_HOST}")
    conn = psycopg2.connect(
        host=DB_HOST, 
        database="desafio3_db", 
        user="user_app", 
        password="app_password"
    )
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS acessos (id SERIAL PRIMARY KEY, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        conn.commit()
    print("Conexões estabelecidas com sucesso!")

for i in range(5):
    try:
        init_connections()
        break
    except Exception as e:
        print(f"Erro na conexão, tentando novamente em 5s: {e}")
        sleep(5)
else:
    raise ConnectionError("Falha ao conectar a todos os serviços após várias tentativas.")


@app.route('/')
def index():
    with conn.cursor() as cur:
        cur.execute("INSERT INTO acessos DEFAULT VALUES;")
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM acessos;")
        total_acessos_db = cur.fetchone()[0]
    
    r.incr('contador_cache')
    acessos_cache = r.get('contador_cache').decode('utf-8')

    return (
        f"<h1>Orquestração de Microsserviços Desafio 3</h1>"
        f"<h2>DB (PostgreSQL)</h2>"
        f"<p>Total de acessos registrados no banco: <b>{total_acessos_db}</b></p>"
        f"<h2>Cache (Redis)</h2>"
        f"<p>Contador de acessos no cache: <b>{acessos_cache}</b></p>"
        f"<p>Status: Comunicação entre os 3 serviços funcionando!</p>"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)