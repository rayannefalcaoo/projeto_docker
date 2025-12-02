import requests
from time import sleep
import os

SERVICE_A_HOST = os.environ.get('SERVICE_A_HOST', 'service-a')
SERVICE_A_URL = f"http://{SERVICE_A_HOST}:8080/users"

def consume_service_a():
    try:
        response = requests.get(SERVICE_A_URL)
        response.raise_for_status() 
        
        users = response.json()
        output = "--- Informações Combinadas ---\n"
        
        for user in users:
            output += f"Usuário {user['nome']} ativo desde {user['ativo_desde']}.\n"
        output += "------------------------------\n"
        return output
        
    except requests.exceptions.ConnectionError:
        return f"❌ Erro de Conexão: O Microsserviço A ({SERVICE_A_URL}) não está acessível. Tentando novamente..."
    except Exception as e:
        return f"❌ Erro ao processar dados: {e}"

while True:
    print(consume_service_a())
    sleep(5)