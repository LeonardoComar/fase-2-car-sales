# 🚗 Car Sales API - Sistema de Vendas de Veículos - Fase 2

## 📋 Sobre o Projeto

O **Car Sales API** é um sistema completo para gerenciamento de vendas de veículos (carros e motocicletas) desenvolvido em **Python** com **FastAPI**. O projeto implementa uma arquitetura clean architecture garantindo separação clara de responsabilidades e facilidade de manutenção.

### ✨ Principais Funcionalidades

- **🚗 Gestão de Veículos**: CRUD completo para carros e motocicletas
- **👥 Gestão de Clientes**: Cadastro e gerenciamento de clientes
- **👨‍💼 Gestão de Funcionários**: Controle de colaboradores
- **💰 Gestão de Vendas**: Registro e acompanhamento de vendas
- **💬 Sistema de Mensagens**: Comunicação com clientes e atribuição de responsáveis
- **📸 Upload de Imagens**: Sistema completo de imagens para veículos com thumbnails
- **🔍 Filtros Avançados**: Busca por preço, status, data, etc.
- **📊 Paginação**: Listagem otimizada com skip/limit

## 🏗️ Arquitetura e Tecnologias

### 📐 Arquitetura Clean Architecture
```
├── app/
│   ├── config/            # Configurações de logging e ambiente
│   └── src/
│       ├── main.py        # Entrypoint da aplicação
│       ├── adapters/      # Adapters (layer de entrada/saída)
│       │   ├── rest/      # Routers, controllers, presenters (entrada HTTP)
│       │   └── persistence/# Gateways e integrações com repositórios (saída)
│       ├── application/   # Casos de uso, DTOs, módulos e serviços de aplicação
│       │   ├── dtos/
│       │   ├── services/
│       │   └── use_cases/
│       ├── domain/        # Entidades, portas (interfaces), repositórios e serviços de domínio
│       │   ├── entities/
│       │   ├── ports/
│       │   ├── repositories/
│       │   └── services/
│       ├── infrastructure/ # Implementações de infraestrutura, DB, adapters e startup
│       │   ├── adapters/
│       │   │   ├── driving/ # Controllers/adapters de entrada usados pela infra
│       │   │   └── driven/  # Implementações de persistência/integração
│       │   ├── config/
│       │   ├── database/
│       │   └── startup/
│       └── tests/         # Testes unitários e de integração

├── Domain (Domínio)
│   ├── entities/          # Entidades de negócio (modelos de domínio)
│   ├── ports/             # Interfaces (contratos) para repositórios e serviços
│   └── services/          # Regras e utilitários de domínio

├── Application (Aplicação)
│   ├── dtos/              # Data Transfer Objects (entrada/saída)
│   ├── use_cases/         # Casos de uso (lógica de aplicação)
│   └── services/          # Serviços de aplicação (coordenação)

└── Infrastructure (Infraestrutura)
    ├── adapters/driving/  # Controllers / Routers / Gateways usados pela camada de entrada
    └── adapters/driven/   # Implementações de persistência e integrações externas
```

### 🛠️ Stack Tecnológico

- **🐍 Python 3.13** - Linguagem principal
- **⚡ FastAPI** - Framework web moderno e rápido
- **🗄️ MySQL 8.0** - Banco de dados relacional
- **📊 SQLAlchemy** - ORM para Python
- **✅ Pydantic** - Validação de dados
- **🐳 Docker, Docker Compose & K8s** - Containerização
- **🖼️ Pillow (PIL)** - Processamento de imagens
- **📝 Swagger/OpenAPI** - Documentação automática da API

## 🚀 Como Usar Localmente

### 📋 Pré-requisitos

- **Docker** e **Docker Compose** instalados
- **Git** para clonar o repositório

### 🔧 Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/LeonardoComar/fase-2-car-sales.git
   cd fase-2-car-sales
   ```

2. **Configure as variáveis de ambiente:**
   ```bash
   # Renomeie o arquivo de exemplo para .env
   cp .env.example .env
   ```

3. **Inicie a aplicação:**
   ```bash
   docker compose up
   ```

   Ou para executar em background:
   ```bash
   docker compose up -d
   ```

### 🌐 Acessos

| Serviço | URL | Descrição |
|---------|-----|-----------|
| 🌐 **API Principal** | http://localhost:8180 | Endpoint base da API |
| 📖 **Documentação Swagger** | http://localhost:8180/docs | Interface interativa da API |
| 📋 **ReDoc** | http://localhost:8180/redoc | Documentação alternativa |

### � Autenticação Automática

A aplicação cria automaticamente um usuário administrador na primeira execução:

| Campo | Valor |
|-------|--------|
| 📧 **Email** | `admin@carsales.com` |
| 🔑 **Senha** | `admin123456` |
| 👑 **Perfil** | Administrador |

### �📮 Postman
1. Importe as collections da pasta `📁 Postman/`:
   - `Car Sales.postman_collection.json` - Todas as requisições
   - `Car Sales.postman_environment.json` - Variáveis de ambiente

#### 🔧 **Configuração Automática de Token no Postman:**
- ✅ **Script de Login Automático** - A rota de login captura automaticamente o token JWT
- ✅ **Variável de Ambiente** - Token é salvo como `{{access_token}}`
- ✅ **Headers Pré-configurados** - Todas as rotas protegidas já incluem `Authorization: Bearer {{access_token}}`
- ✅ **Renovação Automática** - Basta fazer login novamente para atualizar o token

## 📚 Documentação Adicional

### 📖 Documentação Completa
- **📄 PDF:** `Documentação/Documentação.pdf`
- **📝 Word:** `Documentação/Documentação.docx`
- **🎯 Domain Storytelling:** `Documentação/Domain Storytelling/`

# Subir a aplicação
docker compose up -d

# Parar a aplicação
docker compose down

# Remover volume do banco (resetar dados)
docker volume rm fase-2-car-sales_db_carsales_data

## CI/CD e Imagem Docker

- Imagem pública usada nos manifests Kubernetes: `leocomar/carsales:latest`
- O workflow GitHub Actions (`.github/workflows/ci-cd.yaml`) faz build e push para essa imagem.

Secrets necessários no GitHub:
- `DOCKERHUB_TOKEN` — token do Docker Hub (é recomendado criar um Access Token em Docker Hub > Settings > Security)