# Desafio 3 - Orquestração de Microsserviços com Cache

## Descrição da Solução

Este desafio implementa uma arquitetura de microsserviços orquestrada com Docker Compose, demonstrando integração entre uma aplicação web Flask, um banco de dados PostgreSQL e um cache Redis.

### Arquitetura

A solução consiste em três serviços interconectados:

- **Web (Flask)**: Aplicação web que coordena acesso ao banco e cache
- **PostgreSQL**: Banco de dados para persistência de acessos
- **Redis**: Cache em memória para contadores rápidos

### Decisões Técnicas

- **Flask**: Framework web Python para a aplicação principal
- **PostgreSQL 14 Alpine**: Banco de dados relacional para persistência
- **Redis 6 Alpine**: Cache em memória para operações rápidas
- **Variáveis de ambiente**: Configuração flexível via `REDIS_HOST` e `DB_HOST`
- **Retry logic**: Tentativas de conexão com backoff para garantir inicialização
- **Rede compartilhada**: Todos os serviços na mesma rede para comunicação

## Funcionamento Detalhado

### Containers

1. **Container `web` (Flask)**:
   - Aplicação web que expõe uma interface HTML
   - Porta: 5000 (mapeada para 5000 no host)
   - Conecta-se ao PostgreSQL e Redis via variáveis de ambiente
   - Implementa lógica de retry para conexões (até 5 tentativas)
   - Cria tabela `acessos` automaticamente se não existir
   - Incrementa contador no Redis a cada acesso
   - Registra cada acesso no PostgreSQL

2. **Container `db` (PostgreSQL)**:
   - Imagem: `postgres:14-alpine`
   - Credenciais:
     - Usuário: `user_app`
     - Senha: `app_password`
     - Database: `desafio3_db`
   - Volume persistente: `db-data`
   - Armazena histórico de acessos na tabela `acessos`

3. **Container `cache` (Redis)**:
   - Imagem: `redis:6-alpine`
   - Porta padrão: 6379 (não exposta externamente)
   - Armazena contador de acessos em memória
   - Chave: `contador_cache`

### Rede

- **Nome**: `app-net`
- **Tipo**: Bridge
- **Funcionalidade**: Permite comunicação entre todos os serviços
  - Web acessa DB via `db:5432`
  - Web acessa Redis via `cache:6379`

### Volumes

- **Nome**: `db-data`
- **Mapeamento**: `/var/lib/postgresql/data` no container
- **Funcionalidade**: Persiste os dados do PostgreSQL

### Fluxo de Requisição

1. **Usuário acessa** `http://localhost:5000`
2. **Web recebe requisição** na rota `/`
3. **Web insere registro** na tabela `acessos` do PostgreSQL
4. **Web conta total** de acessos no PostgreSQL
5. **Web incrementa contador** no Redis
6. **Web lê contador** do Redis
7. **Web retorna HTML** com informações de ambos os serviços

### Inicialização

1. Docker Compose cria rede `app-net` e volume `db-data`
2. Containers `db` e `cache` são iniciados
3. Container `web` aguarda `db` e `cache` (via `depends_on`)
4. Web tenta conectar (até 5 vezes com intervalo de 5s)
5. Web cria tabela `acessos` se necessário
6. Web inicializa contador no Redis como 0
7. Sistema está pronto para receber requisições

## Instruções de Execução

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passo a Passo

1. **Navegue até o diretório do desafio**:
```bash
cd desafio3
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

4. **Acesse a aplicação no navegador**:
```
http://localhost:5000
```

Ou via linha de comando:
```bash
curl http://localhost:5000
```

5. **Visualize os logs**:
```bash
docker-compose logs -f
```

Para ver logs de um serviço específico:
```bash
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f cache
```

6. **Teste múltiplos acessos**:
   - Recarregue a página várias vezes
   - Observe que:
     - O contador do Redis incrementa a cada acesso
     - O total de acessos no PostgreSQL aumenta
     - Os valores podem diferir se o Redis for reiniciado (dados em memória)

7. **Parar os containers**:
```bash
docker-compose down
```

### Verificações

- ✅ Todos os três containers devem estar em execução
- ✅ A aplicação web deve responder na porta 5000
- ✅ Os dados devem ser salvos no PostgreSQL
- ✅ O contador deve incrementar no Redis
- ✅ A página deve exibir informações de ambos os serviços

### Testando Comportamento

1. **Teste de persistência do PostgreSQL**:
   - Faça alguns acessos
   - Pare os containers: `docker-compose down`
   - Suba novamente: `docker-compose up -d`
   - Os dados do PostgreSQL devem persistir (total de acessos mantido)

2. **Teste de cache em memória (Redis)**:
   - Faça alguns acessos e anote o contador
   - Pare e remova o container Redis: `docker-compose stop cache && docker-compose rm -f cache`
   - Suba novamente: `docker-compose up -d`
   - O contador do Redis volta a 0 (dados em memória são perdidos)

3. **Teste de resiliência**:
   - Pare o banco: `docker-compose stop db`
   - Tente acessar a aplicação (deve falhar)
   - Suba o banco novamente: `docker-compose start db`
   - A aplicação deve voltar a funcionar

