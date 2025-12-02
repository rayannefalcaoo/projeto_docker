# Desafio 5 - API Gateway com Microsserviços

## Descrição da Solução

Este desafio implementa um padrão de API Gateway, onde um único ponto de entrada (gateway) roteia requisições para múltiplos microsserviços backend, demonstrando uma arquitetura de microsserviços escalável e organizada.

### Arquitetura

A solução consiste em três serviços:

- **API Gateway**: Ponto de entrada único que roteia requisições para os serviços apropriados
- **User Service**: Microsserviço que gerencia dados de usuários
- **Order Service**: Microsserviço que gerencia dados de pedidos

### Decisões Técnicas

- **API Gateway Pattern**: Centraliza o roteamento e simplifica o acesso aos microsserviços
- **Roteamento baseado em prefixo**: Requisições para `/users/*` vão para User Service, `/orders/*` para Order Service
- **Proxy reverso**: Gateway atua como proxy, repassando requisições e respostas
- **Isolamento de serviços**: Cada microsserviço roda em sua própria porta interna
- **Rede isolada**: Todos os serviços na mesma rede Docker para comunicação interna
- **Flask + requests**: Gateway usa Flask para receber requisições e requests para fazer proxy

## Funcionamento Detalhado

### Containers

1. **Container `api-gateway`**:
   - Porta exposta: 8000 (mapeada para porta 80 interna)
   - Recebe todas as requisições HTTP
   - Roteia baseado no caminho da URL:
     - `/users/*` → `http://user-service:8001/*`
     - `/orders/*` → `http://order-service:8002/*`
   - Repassa método HTTP, headers, dados e cookies
   - Retorna resposta do serviço backend
   - Trata erros de conexão (503 Service Unavailable)

2. **Container `user-service`**:
   - Porta interna: 8001 (não exposta externamente)
   - Endpoint: `GET /users`
   - Retorna lista de usuários em formato JSON
   - Dados de exemplo: Maria e João

3. **Container `order-service`**:
   - Porta interna: 8002 (não exposta externamente)
   - Endpoint: `GET /orders`
   - Retorna lista de pedidos em formato JSON
   - Dados de exemplo: Teclado e Mouse

### Rede

- **Nome**: `api-gateway-net`
- **Tipo**: Bridge
- **Funcionalidade**: Permite comunicação entre todos os serviços
  - Gateway acessa User Service via `user-service:8001`
  - Gateway acessa Order Service via `order-service:8002`
  - Serviços não são acessíveis externamente, apenas através do gateway

### Fluxo de Requisição

1. **Cliente faz requisição** para `http://localhost:8000/users`
2. **Gateway recebe** a requisição na rota `/<path:path>`
3. **Gateway identifica** que o path começa com `users`
4. **Gateway monta URL** destino: `http://user-service:8001/users`
5. **Gateway faz proxy** da requisição para o User Service
6. **User Service processa** e retorna resposta JSON
7. **Gateway repassa** a resposta para o cliente
8. **Cliente recebe** os dados de usuários

O mesmo fluxo ocorre para `/orders`, mas roteando para o Order Service.

### Roteamento

O gateway usa lógica de prefixo para rotear:

- **Path `/users` ou `/users/*`** → User Service (`http://user-service:8001`)
- **Path `/orders` ou `/orders/*`** → Order Service (`http://order-service:8002`)
- **Outros paths** → Retorna 404 (Rota desconhecida)

### Dependências

- Gateway depende de ambos os serviços (`depends_on`)
- Gateway aguarda User Service e Order Service estarem prontos
- Se um serviço backend não estiver disponível, gateway retorna 503

## Instruções de Execução

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passo a Passo

1. **Navegue até o diretório do desafio**:
```bash
cd desafio5
```

2. **Suba todos os containers**:
```bash
docker-compose up
```

Ou para executar em background:
```bash
docker-compose up -d
```

3. **Aguarde alguns segundos** para todos os serviços inicializarem

4. **Teste o User Service através do Gateway**:
```bash
curl http://localhost:8000/users
```

Resposta esperada:
```json
{
  "service": "User Service (MS1)",
  "data": [
    {"id": 1, "name": "Maria"},
    {"id": 2, "name": "João"}
  ]
}
```

5. **Teste o Order Service através do Gateway**:
```bash
curl http://localhost:8000/orders
```

Resposta esperada:
```json
{
  "service": "Order Service (MS2)",
  "data": [
    {"id": 101, "item": "Teclado"},
    {"id": 102, "item": "Mouse"}
  ]
}
```

6. **Teste rota inexistente**:
```bash
curl http://localhost:8000/products
```

Resposta esperada:
```json
{
  "message": "Rota desconhecida pelo Gateway."
}
```

7. **Visualize os logs**:
```bash
docker-compose logs -f
```

Para ver logs de um serviço específico:
```bash
docker-compose logs -f api-gateway
docker-compose logs -f user-service
docker-compose logs -f order-service
```

8. **Parar os containers**:
```bash
docker-compose down
```

### Verificações

- ✅ Todos os três containers devem estar em execução
- ✅ O gateway deve responder na porta 8000
- ✅ Requisições para `/users` devem retornar dados do User Service
- ✅ Requisições para `/orders` devem retornar dados do Order Service
- ✅ Rotas desconhecidas devem retornar 404
- ✅ Os serviços backend não devem ser acessíveis diretamente do host

### Testando Funcionalidades

1. **Teste de roteamento**:
   - Faça requisições para `/users` e `/orders`
   - Verifique que cada uma vai para o serviço correto
   - Observe os logs do gateway para ver o roteamento

2. **Teste de resiliência**:
   - Pare o User Service: `docker-compose stop user-service`
   - Tente acessar `/users` (deve retornar 503)
   - Suba novamente: `docker-compose start user-service`
   - A requisição deve voltar a funcionar

3. **Teste de isolamento**:
   - Tente acessar diretamente os serviços (não deve funcionar):
   ```bash
   curl http://localhost:8001/users  # Deve falhar
   curl http://localhost:8002/orders  # Deve falhar
   ```
   - Apenas através do gateway deve funcionar

### Arquitetura de Produção

Em um ambiente de produção, esta arquitetura pode ser expandida com:

- **Load Balancer**: Distribuir carga entre múltiplas instâncias de cada serviço
- **Service Discovery**: Descobrir serviços dinamicamente
- **Autenticação/Autorização**: No gateway antes de rotear
- **Rate Limiting**: Limitar requisições por cliente
- **Logging e Monitoramento**: Centralizar logs e métricas
- **Circuit Breaker**: Proteger contra falhas em cascata
- **Health Checks**: Verificar saúde dos serviços backend

### Estrutura de Respostas

**User Service** (`/users`):
```json
{
  "service": "User Service (MS1)",
  "data": [
    {"id": 1, "name": "Maria"},
    {"id": 2, "name": "João"}
  ]
}
```

**Order Service** (`/orders`):
```json
{
  "service": "Order Service (MS2)",
  "data": [
    {"id": 101, "item": "Teclado"},
    {"id": 102, "item": "Mouse"}
  ]
}
```

