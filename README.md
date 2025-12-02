# Projeto 2 - Desafios Docker

Este projeto contém 5 desafios práticos de Docker e orquestração de containers, demonstrando diferentes conceitos e padrões de arquitetura de microsserviços.

## 📋 Desafios

### Desafio 1 - Comunicação Cliente-Servidor
Demonstra comunicação básica entre containers usando Flask e curl, com rede Docker personalizada.

### Desafio 2 - Persistência de Dados com PostgreSQL
Implementa persistência de dados usando PostgreSQL com volumes Docker e healthchecks.

### Desafio 3 - Orquestração de Microsserviços com Cache
Arquitetura com Flask, PostgreSQL e Redis, demonstrando integração entre múltiplos serviços.

### Desafio 4 - Comunicação entre Microsserviços
Dois microsserviços independentes se comunicando via HTTP, demonstrando padrão de consumo de APIs.

### Desafio 5 - API Gateway com Microsserviços
Padrão de API Gateway roteando requisições para múltiplos microsserviços backend.

## 🚀 Como Usar

Cada desafio possui seu próprio diretório com instruções detalhadas:

```bash
# Navegue até o desafio desejado
cd desafio1  # ou desafio2, desafio3, desafio4, desafio5

# Execute os containers
docker-compose up
```

Para mais detalhes sobre cada desafio, consulte o arquivo `README.md` dentro de cada diretório.

## 📁 Estrutura do Projeto

```
Projeto Ray/
├── desafio1/          # Cliente-Servidor
├── desafio2/          # Persistência PostgreSQL
├── desafio3/          # Orquestração com Cache
├── desafio4/          # Comunicação entre Microsserviços
└── desafio5/          # API Gateway
```

## ⚙️ Pré-requisitos

- Docker instalado
- Docker Compose instalado

## 📚 Tecnologias Utilizadas

- **Python 3.13**
- **Flask** - Framework web
- **PostgreSQL** - Banco de dados relacional
- **Redis** - Cache em memória
- **Docker & Docker Compose** - Containerização e orquestração

