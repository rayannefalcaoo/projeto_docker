# Desafio 4 - Comunicação entre Microsserviços

## Descrição da Solução

Este desafio demonstra comunicação entre dois microsserviços independentes, onde um serviço consome APIs do outro através de uma rede Docker compartilhada.

### Arquitetura

A solução consiste em dois microsserviços:

- **Service A**: API REST que fornece dados de usuários
- **Service B**: Consumidor que faz requisições periódicas ao Service A e processa os dados

### Decisões Técnicas

- **Flask**: Framework web leve para ambos os serviços
- **requests**: Biblioteca Python para fazer requisições HTTP entre serviços
- **Comunicação via rede Docker**: Serviços se comunicam usando nomes de containers como DNS
- **Polling**: Service B faz requisições periódicas (a cada 5 segundos)
- **Tratamento de erros**: Service B trata erros de conexão e exibe mensagens apropriadas
- **Variáveis de ambiente**: Service B usa `SERVICE_A_HOST` para flexibilidade

## Funcionamento Detalhado

### Containers

1. **Container `service-a`**:
   - API REST Flask na porta 8080
   - Endpoint: `GET /users`
   - Retorna lista de usuários em formato JSON
   - Dados estáticos de exemplo (Alice, Bob, Carol)
   - Não expõe porta externamente (apenas na rede Docker)

2. **Container `service-b`**:
   - Consumidor que executa em loop contínuo
   - Faz requisições HTTP GET para `http://service-a:8080/users`
   - Processa e exibe os dados recebidos
   - Aguarda 5 segundos entre requisições
   - Trata erros de conexão e exibe mensagens apropriadas
   - Usa variável de ambiente `SERVICE_A_HOST` (padrão: `service-a`)

### Rede

Os serviços precisam estar na mesma rede Docker para se comunicarem. Como não há `docker-compose.yml` neste desafio, os containers devem ser executados manualmente ou criados com uma rede compartilhada.

### Fluxo de Execução

1. **Service A** inicia e fica escutando na porta 8080
2. **Service B** inicia e tenta conectar ao Service A
3. **Service B** faz requisição GET para `/users` a cada 5 segundos
4. **Service A** responde com JSON contendo lista de usuários
5. **Service B** processa os dados e exibe no console
6. O ciclo se repete indefinidamente

### Fluxo de Dados

```
Service B → HTTP GET → Service A:8080/users
                ↓
Service A → JSON Response → Service B
                ↓
Service B → Processa e exibe dados
```

## Instruções de Execução

### Pré-requisitos

- Docker instalado
- Docker Compose instalado (opcional, para facilitar)

### Opção 1: Execução Manual com Docker

1. **Crie uma rede Docker**:
```bash
docker network create service-net
```

2. **Suba o Service A**:
```bash
cd service-a
docker build -t service-a .
docker run -d --name service-a --network service-net -p 8080:8080 service-a
cd ..
```

3. **Suba o Service B**:
```bash
cd service-b
docker build -t service-b .
docker run -d --name service-b --network service-net service-b
cd ..
```

4. **Visualize os logs**:
```bash
docker logs -f service-b
```

5. **Teste o Service A diretamente**:
```bash
curl http://localhost:8080/users
```

6. **Parar os containers**:
```bash
docker stop service-a service-b
docker rm service-a service-b
docker network rm service-net
```

### Opção 2: Criar docker-compose.yml (Recomendado)

Crie um arquivo `docker-compose.yml` na raiz do desafio4:

```yaml
services:
  service-a:
    build: ./service-a
    container_name: service-a
    ports:
      - "8080:8080"
    networks:
      - service-net
    restart: always

  service-b:
    build: ./service-b
    container_name: service-b
    environment:
      SERVICE_A_HOST: service-a
    networks:
      - service-net
    depends_on:
      - service-a
    restart: always

networks:
  service-net:
    driver: bridge
```

Depois execute:

1. **Navegue até o diretório do desafio**:
```bash
cd desafio4
```

2. **Suba os containers**:
```bash
docker-compose up
```

Ou em background:
```bash
docker-compose up -d
```

3. **Visualize os logs**:
```bash
docker-compose logs -f service-b
```

4. **Teste o Service A**:
```bash
curl http://localhost:8080/users
```

5. **Parar os containers**:
```bash
docker-compose down
```

### Verificações

- ✅ Service A deve estar respondendo na porta 8080
- ✅ Service B deve estar fazendo requisições a cada 5 segundos
- ✅ Service B deve exibir os dados processados dos usuários
- ✅ A comunicação entre containers deve funcionar via rede Docker

### Testando Resiliência

1. **Teste de desconexão**:
   - Pare o Service A: `docker stop service-a`
   - Observe que Service B exibe mensagens de erro
   - Suba o Service A novamente: `docker start service-a`
   - Service B deve voltar a funcionar normalmente

2. **Teste de mudança de hostname**:
   - Pare os containers
   - Modifique a variável `SERVICE_A_HOST` no docker-compose.yml
   - Suba novamente e verifique se a comunicação funciona

### Estrutura de Dados

O Service A retorna JSON no formato:
```json
[
  {"id": 1, "nome": "Alice", "ativo_desde": "2023-01-15"},
  {"id": 2, "nome": "Bob", "ativo_desde": "2023-03-20"},
  {"id": 3, "nome": "Carol", "ativo_desde": "2023-05-10"}
]
```

O Service B processa e exibe:
```
--- Informações Combinadas ---
Usuário Alice ativo desde 2023-01-15.
Usuário Bob ativo desde 2023-03-20.
Usuário Carol ativo desde 2023-05-10.
------------------------------
```

