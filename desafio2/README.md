# Desafio 2 - Persistência de Dados com PostgreSQL

## Descrição da Solução

Este desafio demonstra persistência de dados usando PostgreSQL com volumes Docker, incluindo inicialização automática do banco de dados e um serviço de leitura que verifica a persistência dos dados.

### Arquitetura

A solução consiste em dois serviços:

- **PostgreSQL**: Banco de dados que armazena dados de forma persistente usando volumes Docker
- **Reader**: Serviço Python que lê dados do banco para comprovar a persistência

### Decisões Técnicas

- **PostgreSQL 14 Alpine**: Versão leve e estável do PostgreSQL
- **Volumes Docker**: Garantem que os dados persistem mesmo após remoção dos containers
- **Healthcheck**: Verifica se o PostgreSQL está pronto antes de iniciar o reader
- **Script de inicialização**: SQL executado automaticamente na primeira inicialização
- **Profiles**: O reader usa profile para permitir execução opcional
- **psycopg2**: Biblioteca Python para conexão com PostgreSQL

## Funcionamento Detalhado

### Containers

1. **Container `db` (PostgreSQL)**:
   - Imagem: `postgres:14-alpine`
   - Credenciais:
     - Usuário: `user_desafio`
     - Senha: `pass_desafio`
     - Database: `desafio2_db`
   - Volume persistente: `dados_persistentes_desafio2`
   - Script de inicialização: `./db/setup.sql` (executado automaticamente)
   - Healthcheck: Verifica se o PostgreSQL está pronto a cada 5 segundos
   - Restart: Sempre reinicia automaticamente

2. **Container `reader`**:
   - Baseado em Python 3.13
   - Conecta ao PostgreSQL após o healthcheck confirmar que está pronto
   - Lê o primeiro registro da tabela `persistencia`
   - Exibe mensagem de sucesso ou erro
   - Profile: `reader` (pode ser executado opcionalmente)

### Rede

- **Nome**: `persistence-net`
- **Tipo**: Bridge
- **Funcionalidade**: Permite comunicação entre o reader e o banco de dados

### Volumes

- **Nome**: `dados_persistentes_desafio2`
- **Mapeamento**: `/var/lib/postgresql/data` no container
- **Funcionalidade**: Persiste os dados do PostgreSQL mesmo após remoção dos containers

### Script de Inicialização

O arquivo `setup.sql` é executado automaticamente na primeira inicialização do banco:

- Cria a tabela `persistencia` se não existir
- Insere um registro inicial com mensagem e timestamp

### Fluxo de Execução

1. O Docker Compose cria a rede `persistence-net` e o volume `dados_persistentes_desafio2`
2. O container `db` é iniciado e executa o script `setup.sql`
3. O healthcheck verifica se o PostgreSQL está pronto
4. Após o healthcheck passar, o container `reader` é iniciado
5. O reader aguarda 5 segundos e tenta conectar ao banco
6. O reader lê o primeiro registro da tabela `persistencia`
7. O reader exibe mensagem de sucesso ou erro e encerra

## Instruções de Execução

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passo a Passo

1. **Navegue até o diretório do desafio**:
```bash
cd desafio2
```

2. **Suba apenas o banco de dados**:
```bash
docker-compose up -d db
```

3. **Aguarde alguns segundos para o banco inicializar completamente**

4. **Execute o reader para verificar a persistência**:
```bash
docker-compose --profile reader up reader
```

Ou para executar tudo de uma vez:
```bash
docker-compose --profile reader up
```

5. **Visualize os logs**:
```bash
docker-compose logs -f
```

6. **Teste a persistência**:
   - Pare os containers: `docker-compose down`
   - Suba novamente: `docker-compose --profile reader up`
   - Os dados devem persistir mesmo após remover os containers

7. **Parar os containers**:
```bash
docker-compose down
```

### Verificações

- ✅ O PostgreSQL deve inicializar com sucesso
- ✅ O script `setup.sql` deve criar a tabela e inserir dados
- ✅ O reader deve conseguir conectar e ler os dados
- ✅ Os dados devem persistir após remover e recriar os containers

### Testando Persistência

Para comprovar que os dados persistem:

1. Suba o banco: `docker-compose up -d db`
2. Execute o reader: `docker-compose --profile reader up reader`
3. Anote a mensagem e timestamp exibidos
4. Pare tudo: `docker-compose down`
5. Suba novamente: `docker-compose --profile reader up`
6. Os mesmos dados devem aparecer, comprovando a persistência

