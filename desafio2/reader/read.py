import psycopg2, os
from time import sleep

DB_HOST = 'db' 
DB_USER = 'user_desafio'
DB_PASSWORD = 'pass_desafio'
DB_NAME = 'desafio2_db'

print("--- Tentando conectar ao PostgreSQL ---")

try:
    sleep(5) 
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    cur = conn.cursor()
    
    cur.execute("SELECT mensagem, criado_em FROM persistencia ORDER BY criado_em ASC LIMIT 1;")
    dado = cur.fetchone()
    
    if dado:
        print("\n✅ Persistência COMPROVADA com sucesso! ✅")
        print(f"Mensagem lida: {dado[0]}")
        print(f"Criado em: {dado[1]}")
    else:
        print("\n❌ ERRO: Nenhuma dado encontrado na tabela. ❌")
        
    cur.close()
    conn.close()

except Exception as e:
    print(f"\n❌ ERRO FATAL de Conexão ou Leitura: {e} ❌")
    exit(1)

exit(0)