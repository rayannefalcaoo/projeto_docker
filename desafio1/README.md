# Desafio 1 - Comunicação Cliente-Servidor

## Descrição da Solução

Este desafio implementa uma arquitetura cliente-servidor básica usando Docker Compose, demonstrando comunicação entre containers através de uma rede Docker personalizada.

### Arquitetura

A solução consiste em dois containers:

- **Servidor (Flask)**: Aplicação web Python que responde a requisições HTTP na porta 8080
- **Cliente (curl)**: Container que faz requisições periódicas ao servidor a cada 3 segundos

### Decisões Técnicas

- **Flask**: Framework web leve e simples para Python, ideal para demonstrar comunicação HTTP
- **curl**: Ferramenta de linha de comando para fazer requisições HTTP, encapsulada em container
- **Rede Docker Bridge**: Rede isolada (`rede-projeto2`) que permite comunicação entre containers usando nomes de serviço como DNS
- **Hostname customizado**: O servidor usa o hostname `server` para facilitar a resolução de nomes

## Funcionamento Detalhado

### Containers

1. **Container `server`**:
   - Baseado em `python:3.13`
   - Executa uma aplicação Flask na porta 8080
   - Expõe a porta 8080 para o host (mapeada para 8080)
   - Responde na rota `/` com uma mensagem contendo o ID do container
   - Hostname: `server`

2. **Container `client`**:
   - Baseado em `curlimages/curl`
   - Executa um loop infinito que:
     - Faz requisição HTTP GET para `http://servidor:8080`
     - Exibe a resposta
     - Aguarda 3 segundos antes da próxima requisição
   - Depende do container `servidor` estar em execução

### Rede

- **Nome**: `rede-projeto2`
- **Tipo**: Bridge (padrão do Docker)
- **Funcionalidade**: Permite que os containers se comuniquem usando os nomes de serviço como endereços DNS
  - O cliente acessa o servidor através de `http://servidor:8080`
  - O Docker resolve automaticamente `servidor` para o IP do container

### Fluxo de Execução

1. O Docker Compose inicia a rede `rede-projeto2`
2. O container `servidor` é iniciado e fica escutando na porta 8080
3. O container `cliente` é iniciado após o servidor (devido ao `depends_on`)
4. O cliente começa a fazer requisições HTTP GET a cada 3 segundos
5. O servidor responde com uma mensagem contendo seu hostname/ID
6. O cliente exibe a resposta no console

## Instruções de Execução

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passo a Passo

1. **Navegue até o diretório do desafio**:
```bash
cd desafio1
```

2. **Suba os containers**:
```bash
docker-compose up
```

Ou para executar em background:
```bash
docker-compose up -d
```

3. **Visualize os logs**:
```bash
docker-compose logs -f
```

Para ver logs de um container específico:
```bash
docker-compose logs -f cliente
docker-compose logs -f servidor
```

4. **Teste manualmente o servidor**:
Abra um novo terminal e faça uma requisição:
```bash
curl http://localhost:8080
```

Você verá uma resposta como:
```
Olá, Mundo! Este é o container: server
```

5. **Parar os containers**:
```bash
docker-compose down
```

### Verificações

- ✅ O servidor deve estar respondendo na porta 8080
- ✅ O cliente deve estar fazendo requisições a cada 3 segundos
- ✅ Os logs do cliente devem mostrar as respostas do servidor
- ✅ A comunicação entre containers deve funcionar através da rede Docker

